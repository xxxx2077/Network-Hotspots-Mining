from app.models import Post, Comments, Summary, Class
from datetime import datetime, timezone
import requests
import json
import time
from django.db import transaction
from ratelimit import sleep_and_retry, limits
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from urllib3.exceptions import InsecureRequestWarning


# 设定每10秒最多1次请求
@sleep_and_retry
@limits(calls=1, period=10)
def Api(content, task):
    # 限制最大 token
    if len(content) > 500:
        content = content[:500]

    # 构建 json 请求
    url = 'https://akita-famous-sincerely.ngrok-free.app/v1/chat/completions'
    data = {
        "messages": [{"role": "user", "content": content}],
        "stream": False,
        "task": task
    }
    headers = {
        "Content-Type": "application/json"
    }

    # 配置重试策略
    retries = Retry(
        total=5,  # 总重试次数
        backoff_factor=1,  # 重试间隔时间的增长因子
        status_forcelist=[500, 502, 503, 504]  # 指定哪些状态码的错误需要重试
    )

    # 使用 Session 对象发送 LLM 请求
    with requests.Session() as session:
        session.mount('https://', HTTPAdapter(max_retries=retries))
        try:
            response = session.post(url=url, json=data, headers=headers)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None

    # 检查响应状态码
    if response.status_code == 200:
        # 获取响应数据
        response_data = response.json()
        generated_text = response_data.get("choices", [])[0].get("message", {}).get("content", "")
        return generated_text
    else:
        print(f"API response error with status code {response.status_code}")
        return None


def LLM_summary(post_id, task="1"):
    try:
        # 访问数据库，获取帖子和评论
        post = Post.objects.get(id=post_id)
        comments = Comments.objects.filter(pid=post_id).order_by('-likeNum').values_list('content', flat=True)
        title = post.title
        content = post.content
        top_comments = list(comments[:3])  # 取前三个

        # 拼接标题
        content = '事件：' + title + '。' + content
        # 拼接评论
        for comment in top_comments:
            content = content + '评论：' + comment + '。'
        # 去掉空格
        content = ''.join(content.split())

        reset_num = 0  # 限制错误重试次数
        while reset_num < 5:
            # 调用 API
            generated_text = Api(content, task)

            # 转为 json
            generated_json = {}
            lines = generated_text.split('\n')

            # 错误1：没有分行
            if len(lines) < 7:
                print('error1:')
                print(post_id)
                print(content)
                print(generated_text)
                print('---')
                content = content + '。注意：每一点后面换行。'
                reset_num += 1
                continue

            # 遍历
            for line in lines:
                if line.startswith("时间：") or line.startswith("1. 时间："):
                    generated_json['date'] = line.split("时间：")[1].strip()
                elif line.startswith("地点：") or line.startswith("2. 地点："):
                    generated_json['location'] = line.split("地点：")[1].strip()
                elif line.startswith("主要参与者：") or line.startswith("3. 主要参与者："):
                    generated_json['participants'] = line.split("主要参与者：")[1].strip()
                elif line.startswith("关键点：") or line.startswith("4. 关键点："):
                    generated_json['Key_points'] = line.split("关键点：")[1].strip()
                elif line.startswith("事件总结：") or line.startswith("5. 事件总结："):
                    generated_json['summary'] = line.split("事件总结：")[1].strip()
                    print(generated_json['summary'])
                elif line.startswith("影响及后果：") or line.startswith("6. 影响及后果："):
                    generated_json['consequences'] = line.split("影响及后果：")[1].strip()
                elif line.startswith("评论观点：") or line.startswith("7. 评论观点："):
                    generated_json['comments'] = line.split("评论观点：")[1].strip()

            # 错误2：格式错误
            if 'summary' not in generated_json:
                print('error2:')
                print(post_id)
                print(content)
                print(generated_text)
                print('---')
                content = content + '。注意：按照以下格式简洁明了地总结这一事件：1. 时间：2. 地点：3. 主要参与者：4. 关键点：5. 事件总结：6. 影响及后果：'
                reset_num += 1
                continue

            # 错误3：没有总结部份
            if (generated_json['summary'] == "N/A") or (generated_json['summary'] == "无") or (
                    generated_json['summary'] == "None"):
                print('error3:')
                print(post_id)
                print(content)
                print(generated_text)
                print('---')
                content = content + '。注意：一定要进行5. 事件总结：'
                reset_num += 1
                continue

            # 成功：存入数据库
            with transaction.atomic():
                summary = Summary(
                    summary_id=int(post_id),
                    date=generated_json.get('date'),
                    location=generated_json.get('location'),
                    participants=generated_json.get('participants'),
                    Key_points=generated_json.get('Key_points'),
                    summary=generated_json.get('summary'),
                    consequences=generated_json.get('consequences'),
                    comments=generated_json.get('comments')
                )
                summary.save()
                Post.objects.filter(id=post_id).update(is_summaried=True)
            print('success:')
            print(post_id)
            print('---')
            break

        # 失败
        if reset_num >= 5:
            with transaction.atomic():
                summary = Summary(
                    summary_id=int(post_id),
                    is_abnormal=True,
                )
                summary.save()
                Post.objects.filter(id=post_id).update(is_summaried=True)
            print('fail:')
            print(post_id)
            print('---')

    # 线程错误
    except Exception as e:
        print(f"Exception occurred for post_id={post_id}: {e}")


def LLM_class(task="2"):
    # 访问 json 文件，获取聚类结果集合
    with open('./app/result/res_total.json', 'r', encoding='utf-8') as file:
        content_list = json.load(file)
    with open('./app/result/res_cluster2hot.json', 'r', encoding='utf-8') as file:
        cluster2hot_list = json.load(file)
    with open('./app/result/res_cluster2hot_perday.json', 'r', encoding='utf-8') as file:
        cluster2hot_perday_list = json.load(file)

    # 遍历每个类别的聚类结果
    for it in content_list:
        print(it)
        # 转换 json 字符串
        content = json.dumps(content_list[it], ensure_ascii=False)

        reset_num = 0  # 限制错误重试次数
        while reset_num < 5:
            # 调用 API
            generated_text = Api(content, task)

            # 转为 json
            generated_json = {}
            lines = generated_text.split('\n')

            # 遍历
            for line in lines:
                if line.startswith("类别标题：") or line.startswith("1. 类别标题："):
                    generated_json['class_title'] = line.split("类别标题：")[1].strip()
                elif line.startswith("关键词：") or line.startswith("2. 关键词："):
                    generated_json['Key_points'] = line.split("关键词：")[1].strip()
                elif line.startswith("事件总结：") or line.startswith("3. 事件总结："):
                    generated_json['summary'] = line.split("事件总结：")[1].strip()

            # 错误1：格式错误
            if 'summary' not in generated_json:
                print('error3:')
                print(generated_text)
                print('---')
                content = '注意：总结出该类别的主要特征，包括但不限于常见1. 类别标题：2. 关键词：3. 事件总结：' + content
                reset_num += 1
                continue

            # 错误2：没有总结部份
            if (generated_json['summary'] == "N/A") or (generated_json['summary'] == "无") or (
                    generated_json['summary'] == "None"):
                print('error2:')
                print(generated_text)
                print('---')
                content = '注意：一定要进行3. 事件总结：' + content
                reset_num += 1
                continue

            # 成功：存入数据库
            hot_value_total = 0.0
            hot_value_perday_total = 0.0
            for hot_value in (cluster2hot_list[it]):
                hot_value_total += float(hot_value)
            for hot_value_perday in (cluster2hot_perday_list[it]):
                hot_value_perday_total += float(hot_value_perday)
            class_ = Class(
                class_id=int(it) + 1,
                class_title=generated_json.get('class_title'),
                Key_points=generated_json.get('Key_points'),
                summary=generated_json.get('summary'),
                hot_value=hot_value_total,
                hot_value_perday=hot_value_perday_total
                # is_used=True
            )
            class_.save()
            print('success:')
            print(generated_text)
            print('---')
            break
