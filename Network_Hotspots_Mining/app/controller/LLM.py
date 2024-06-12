from app.models import Post, Summary, Class
import requests
import json
import time


def Api(content, task):
    # 构建 json 请求
    data = {
        "messages": [{"role": "user", "content": content}],
        "stream": False,
        "task": task
    }

    # 发送 POST 到 LLM
    response = requests.post('https://ample-learning-sloth.ngrok-free.app/v1/chat/completions', json=data)

    # 检查响应状态码
    if response.status_code == 200:
        # 获取响应数据
        response_data = response.json()
        generated_text = response_data.get("choices", [])[0].get("message", {}).get("content", "")

        return generated_text
    else:
        return response.status_code


def LLM_summary(task="1"):
    # 访问数据库，获取帖子【之后加上自动监测】
    post = Post.objects.get(id=1813553090)
    id = post.id
    title = post.title
    content = post.content
    # 将标题拼接进去
    content = '标题：' + title + ';' + '事件：' + content

    while True:
        # 调用 API
        generated_text = Api(content, task)

        # 转为 json
        generated_json = {}
        lines = generated_text.split('\n')
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
                if generated_json['summary'] == ('无' or 'NAN' or 'N/A'):
                    continue
            elif line.startswith("影响及后果：") or line.startswith("6. 影响及后果："):
                generated_json['consequences'] = line.split("影响及后果：")[1].strip()
            else:
                continue

        # 存入数据库
        summary = Summary(
            summary_id=int(id),
            date=generated_json.get('date'),
            location=generated_json.get('location'),
            participants=generated_json.get('participants'),
            Key_points=generated_json.get('Key_points'),
            summary=generated_json.get('summary'),
            consequences=generated_json.get('consequences')
        )
        summary.save()
        print(generated_text)
        break


def LLM_class(task="2"):
    # 访问 json 文件，获取聚类结果集合
    with open('./app/result/res_total.json', 'r', encoding='utf-8') as file:
        content_list = json.load(file)

    # 遍历每个类别的聚类结果
    for it in content_list:
        # 转换为 JSON 字符串
        content = json.dumps(content_list[it], ensure_ascii=False)

        while True:
            # 调用 API
            generated_text = Api(content, task)

            # 转为 json
            generated_json = {}
            lines = generated_text.split('\n')
            for line in lines:
                if line.startswith("类别标题：") or line.startswith("1. 类别标题："):
                    generated_json['class_title'] = line.split("类别标题：")[1].strip()
                elif line.startswith("关键词：") or line.startswith("2. 关键词："):
                    generated_json['Key_points'] = line.split("关键词：")[1].strip()
                elif line.startswith("事件总结：") or line.startswith("3. 事件总结："):
                    generated_json['summary'] = line.split("事件总结：")[1].strip()
                    if generated_json['summary'] == ('无' or 'NAN' or 'N/A'):
                        print('error:\n' + generated_text)
                        print('---')
                        continue
                else:
                    print('error:\n'+generated_text)
                    print('---')
                    continue

            # 存入数据库
            class_ = Class(
                class_title=generated_json.get('class_title'),
                Key_points=generated_json.get('Key_points'),
                summary=generated_json.get('summary'),
            )
            class_.save()
            print(generated_text)
            print('---')
            break
