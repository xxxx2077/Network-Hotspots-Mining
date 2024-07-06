from django.db.models import F, OuterRef, Subquery, Sum
from django.db.models.functions import TruncDate
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from app.controller.single_pass import launch_single_pass, get_data
from app.controller.LLM import LLM_summary, LLM_class
from app.models import Comments, Post, Class, PopRecord
from app.util.util import querySet_to_list
from app.misc.data_processing import preprocess_data, mark_used, days_calculating
from app.misc.clear_db import clear_db_class, clear_db_summary
import concurrent.futures
import datetime
import pandas as pd
import os
import json
from django.utils import timezone
from datetime import timedelta
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseBadRequest


# Create your views here.
# def test(request):
#     fuck()
#     return HttpResponse('Hello,world!')


# def preprocess(request):
#     preprocess_data()
#     return HttpResponse('get_data done')


def clear(request):
    # clear_db_summary()
    clear_db_class()
    return HttpResponse('clear has done')


def LLM_summary_db(request):
    print('LLM_summary_db is running...')
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     id_querySet = Post.objects.values('id').all()
    #     id_list = querySet_to_list(id_querySet,'id')
    #     print(id_list)
    #     print('wait for result...')
    #     for id in id_list:
    #         executor.submit(LLM_summary, id)
    #     executor.shutdown()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        id_querySet = Post.objects.filter(is_summaried=False).values('id').order_by('-time')
        id_list = querySet_to_list(id_querySet, 'id')
        print(len(id_list))
        print(id_list)
        print('wait for result...')
        result = executor.map(LLM_summary, id_list)
        # with open(os.path.join(os.path.dirname(__file__),"result/LLM_summary_db_res.txt"), "w", encoding="utf-8") as f:
        #     for res in result:
        #         res = str(res)+'\n'
        #         print(res)
        #         f.write(res)

    return HttpResponse('LLM_summary_db done!')


def LLM(request):
    launch_single_pass()
    LLM_class()

    return HttpResponse('text_cluster_catorizing done!')


'''
主页接口
'''
#判断话题类型函数
def get_topic_type(topic_id):
    # 判断class表中是否有该话题
    if not Class.objects.filter(class_id=topic_id).exists():
        return "未分析"
    
    # 获取对应class_id的所有post记录
    posts = Post.objects.filter(class_id=topic_id).values('correlation', 'sentiment_negative')
    
    # 转换为DataFrame
    posts_df = pd.DataFrame(posts)
    
    if posts_df.empty:
        return 0
    
    # 根据条件分类
    def classify(row):
        if row['correlation'] > 0.75 and row['sentiment_negative'] < -15:
            return 1
        elif row['correlation'] <= 0.75 and row['sentiment_negative'] < -15:
            return 2
        elif row['correlation'] <= 0.7 and row['sentiment_negative'] >= -15:
            return 3
        else:
            return 4
    
    posts_df['category'] = posts_df.apply(classify, axis=1)
    
    # 统计每个分类的数量
    category_counts = posts_df['category'].value_counts().to_dict()
    
    # 判断是否存在舆论预警事件
    if category_counts.get(1, 0) > 0:
        return "舆论预警"
    
    # 计算其余三种事件的数量并返回最多的类型
    two_count = category_counts.get(2, 0)
    three_count = category_counts.get(3, 0)
    four_count = category_counts.get(4, 0)
    
    max_count = max(two_count, three_count, four_count)
    
    if max_count == four_count:
        return "校内热点"
    elif max_count == three_count:
        return "校外热点"
    else:
        return "负面事件"

# 获取热榜
@require_http_methods(["GET"])
def get_hotlist(request):
    # 获取满足条件的前十条记录，按 hot_value 从高到低排序
    class_querySet = Class.objects.filter(hot_value__gte=200).order_by('-hot_value')[:10]

    # 构建返回的数据
    response_data = {
        "data": []
    }

    for cls in class_querySet:
        class_type = get_topic_type(cls.class_id)
        response_data["data"].append({
            "id": cls.class_id,
            "class": class_type,
            "topic": cls.class_title,
            "value": cls.hot_value
        })

    if len(class_querySet) == 10:
        # 尝试获取更多热度大于x值的记录
        additional_querySet = Class.objects.filter(hot_value__gte=200).exclude(
            pk__in=[cls.pk for cls in class_querySet])
        for cls in additional_querySet:
            class_type = get_topic_type(cls.class_id)
            response_data["data"].append({
                "id": cls.class_id,
                "class": class_type,
                "topic": cls.class_title,
                "value": cls.hot_value
            })

    return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})


# 获取热度上升榜
@require_http_methods(["GET"])
def get_speedlist(request):
    # 获取满足条件的前十条记录，按 hot_value_rate 从高到低排序
    class_querySet = Class.objects.filter(hot_value_perday__gte=100).order_by('-hot_value_perday')[:10]

    # 构建返回的数据
    response_data = {
        "data": []
    }
    
    for cls in class_querySet:
        class_type = get_topic_type(cls.class_id)
        response_data["data"].append({
            "id": cls.class_id,
            "class": class_type,
            "topic": cls.class_title,
            "value": cls.hot_value_perday
        })

    if len(class_querySet) == 10:
        # 尝试获取更多热度大于x值的记录
        additional_querySet = Class.objects.filter(hot_value_perday__gte=100).exclude(
            pk__in=[cls.pk for cls in class_querySet])
        for cls in additional_querySet:
            class_type = get_topic_type(cls.class_id)
            response_data["data"].append({
                "id": cls.class_id,
                "class": class_type,
                "topic": cls.class_title,
                "value": cls.hot_value_perday
            })


    return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})


#首页接口3
@require_http_methods(["GET"])
def get_weekly_event_hotval(request):
    
    '''
    注释的是不经过一定热度值筛选
    '''
    # # 获取最近7天的日期
    # end_date = datetime.date.today()
    # start_date = end_date - datetime.timedelta(days=7)
    
    # # 获取最近7天的所有帖子记录
    # posts = Post.objects.filter(time__gte=start_date, time__lt=end_date).values('id', 'time', 'correlation', 'sentiment_negative')
    hotval_threshold = 50  # 设置热度值阈值

    # 获取最近7天的日期
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=7)
    
    # 获取最新的poprecord记录并且hotval大于阈值
    latest_poprecord = PopRecord.objects.filter(
        pid=OuterRef('pk')
    ).order_by('-recordtime')
    
    # 获取最近7天且符合条件的所有帖子记录
    posts = Post.objects.annotate(
        latest_hotval=Subquery(latest_poprecord.values('hotval')[:1])
    ).filter(
        time__gte=start_date,
        time__lt=end_date,
        latest_hotval__gte=hotval_threshold
    ).values('id', 'time', 'correlation', 'sentiment_negative')
    
    # 转换为DataFrame
    posts_df = pd.DataFrame(posts)
    
    if posts_df.empty:
        return JsonResponse({"data": []})
    
    # 将时间转换为日期
    posts_df['date'] = posts_df['time'].dt.date
    
    # 获取相关帖子最新的pop记录
    pop_records = PopRecord.objects.filter(pid__in=posts_df['id']).values('pid', 'hotval', 'recordtime')
    pop_records_df = pd.DataFrame(pop_records).sort_values('recordtime').drop_duplicates('pid', keep='last')
    
    # 合并数据
    merged_df = posts_df.merge(pop_records_df, left_on='id', right_on='pid', how='left')
    
    # 替换缺失的hotval为0
    merged_df['hotval'] = merged_df['hotval'].fillna(0).astype(int)
    
    # 根据条件分类
    def classify(row):
        if row['correlation'] > 0.75 and row['sentiment_negative'] < -15:
            return 1
        elif row['correlation'] <= 0.75 and row['sentiment_negative'] < -15:
            return 2
        elif row['correlation'] <= 0.75 and row['sentiment_negative'] >= -15:
            return 3
        else:
            return 4
    
    merged_df['category'] = merged_df.apply(classify, axis=1)
    
    # 按日期和分类分组并求和
    grouped_df = merged_df.groupby(['date', 'category'])['hotval'].sum().unstack(fill_value=0).reset_index()
    
    # 确保有所有需要的分类
    for category in [1, 2, 3, 4]:
        if category not in grouped_df:
            grouped_df[category] = 0
    
    # 准备返回的数据结构
    data = []
    for _, row in grouped_df.iterrows():
        daily_data = {
            "1": row.get(1, 0),
            "2": row.get(2, 0),
            "3": row.get(3, 0),
            "4": row.get(4, 0),
            "date": row['date'].strftime("%Y-%m-%d")
        }
        data.append(daily_data)
    
    # 返回JSON响应
    return JsonResponse({"data": data})



#首页接口4
@require_http_methods(["GET"])
def get_weekly_event_counts(request):
    
    '''
    注释的是不经过一定热度值筛选
    '''
        
    # end_date = datetime.date.today()
    # start_date = end_date - datetime.timedelta(days=7)
    
    # # 获取最近7天的所有帖子记录
    # posts = Post.objects.filter(time__gte=start_date, time__lt=end_date).values('correlation', 'sentiment_negative')
    
    hotval_threshold = 50  # 设置热度值阈值
    # 获取最近7天的日期
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=7)
    
    # 获取最新的poprecord记录并且hotval大于阈值
    latest_poprecord = PopRecord.objects.filter(
        pid=OuterRef('pk')
    ).order_by('-recordtime')
    
    # 获取最近7天且符合条件的所有帖子记录
    posts = Post.objects.annotate(
        latest_hotval=Subquery(latest_poprecord.values('hotval')[:1])
    ).filter(
        time__gte=start_date,
        time__lt=end_date,
        latest_hotval__gte=hotval_threshold
    ).values('correlation', 'sentiment_negative')
    
    # 转换为DataFrame
    posts_df = pd.DataFrame(posts)
    
    if posts_df.empty:
        return JsonResponse({
            "data": {
                "negative": 0,
                "hotspot": 0,
                "warning": 0,
                "prewarning": 0
            }
        })
    
    # 根据条件分类
    def classify(row):
        if row['correlation'] > 0.75 and row['sentiment_negative'] < -15:
            return 1
        elif row['correlation'] <= 0.75 and row['sentiment_negative'] < -15:
            return 2
        else:
            return 3
    
    posts_df['category'] = posts_df.apply(classify, axis=1)
    
    # 统计每个分类的数量
    category_counts = posts_df['category'].value_counts().to_dict()
    
    # 确保返回的结构中包含所有需要的分类
    result = {
        "negative": category_counts.get(2, 0),
        "hotspot": category_counts.get(3, 0),
        "warning": 0,
        "prewarning": category_counts.get(1, 0)
    }
    
    # 返回JSON响应
    return JsonResponse({"data": result})


#首页接口5
@require_http_methods(["GET"])
def get_weekly_viewnum_stats(request):
    # 获取当前时间和5周前的时间
    now = datetime.date.today()
    start_date = now - timedelta(weeks=5)

    # 从Post表中获取最近5周的帖子记录，并转换为DataFrame
    posts = Post.objects.filter(time__gte=start_date, correlation__gt=0.75).values()
    posts_df = pd.DataFrame(posts)

    if posts_df.empty:
        return JsonResponse({"data": []})

    # 获取PopRecord表中的最新记录，并转换为DataFrame
    poprecords = PopRecord.objects.filter(pid__in=posts_df['id']).values()
    poprecords_df = pd.DataFrame(poprecords)

    if poprecords_df.empty:
        return JsonResponse({"data": []})

    # 只保留每个pid最新的记录
    poprecords_df = poprecords_df.sort_values('recordtime').drop_duplicates('pid', keep='last')

    # 将PopRecord数据合并到Post数据
    merged_df = posts_df.merge(poprecords_df, left_on='id', right_on='pid')

    # 只保留hotval大于50的记录
    merged_df = merged_df[merged_df['hotval'] > 50]

    # 将viewnum置零的无效记录
    merged_df.loc[merged_df['hotval'] <= 30, 'viewnum'] = 0

    # 按时间周和sentiments_negative分类统计viewnum
    merged_df['week'] = merged_df['time'].dt.strftime('%Y-%U')
    negative_df = merged_df[merged_df['sentiment_negative'] < -20].groupby('week')['viewnum'].sum().reset_index()
    hotspot_df = merged_df[merged_df['sentiment_negative'] >= -20].groupby('week')['viewnum'].sum().reset_index()

    # 构建API返回数据
    now_date = datetime.date.today()
    data = []
    for i in range(5):
        week_start = now_date - timedelta(weeks=i)
        week_label = week_start.strftime('%m月第%U周')
        week_key = week_start.strftime('%Y-%U')

        negative_viewnum = negative_df.loc[negative_df['week'] == week_key, 'viewnum'].sum()
        hotspot_viewnum = hotspot_df.loc[hotspot_df['week'] == week_key, 'viewnum'].sum()

        data.append({
            "week": week_label,
            "negative": int(negative_viewnum),
            "hotspot": int(hotspot_viewnum)
        })

    return JsonResponse(data, safe=False)

#首页接口6
@require_http_methods(["GET"])
def get_monthly_viewnum_stats(request):
    # 获取当前时间和6个月前的时间
    now = datetime.date.today()
    start_date = now - timedelta(days=12*30)

    # 从Post表中获取最近6个月的帖子记录，并转换为DataFrame
    posts = Post.objects.filter(time__gte=start_date, correlation__gt=0.75).values()
    posts_df = pd.DataFrame(posts)

    if posts_df.empty:
        return JsonResponse({})

    # 获取PopRecord表中的最新记录，并转换为DataFrame
    poprecords = PopRecord.objects.filter(pid__in=posts_df['id']).values()
    poprecords_df = pd.DataFrame(poprecords)

    if poprecords_df.empty:
        return JsonResponse({"data": []})

    # 只保留每个pid最新的记录
    poprecords_df = poprecords_df.sort_values('recordtime').drop_duplicates('pid', keep='last')

    # 将PopRecord数据合并到Post数据
    merged_df = posts_df.merge(poprecords_df, left_on='id', right_on='pid')

    # 只保留hotval大于50的记录
    merged_df = merged_df[merged_df['hotval'] > 50]

    # 将viewnum置零的无效记录
    merged_df.loc[merged_df['hotval'] <= 30, 'viewnum'] = 0

    # 按月份统计viewnum
    merged_df['month'] = merged_df['time'].dt.strftime('%Y-%m')
    monthly_viewnum = merged_df.groupby('month')['viewnum'].sum().reset_index()

    # 构建API返回数据
    data = []
    for i in range(12):
        month_start = (now - timedelta(days=i*30)).strftime('%Y-%m')
        month_label = (now - timedelta(days=i*30)).strftime('%m月')
        viewnum = monthly_viewnum.loc[monthly_viewnum['month'] == month_start, 'viewnum'].sum()
        data.append({
            "month": month_label,
            "value": int(viewnum) if not monthly_viewnum.loc[monthly_viewnum['month'] == month_start].empty else 0
        })

    return JsonResponse(data, safe=False)

'''
话题详情页面接口
'''


# 获取话题详情
@require_http_methods(["GET"])  # 限制只能使用 GET 方法访问这个视图
def get_topic_details(request):
    # 尝试从GET请求中获取 topicID，并验证其是否为有效整数
    try:
        topic_id = int(request.GET.get('topicID', ''))
    except ValueError:
        # 返回400 Bad Request响应
        return JsonResponse({'error': 'Invalid topicID format'}, status=400)
    if topic_id:
        try:
            # post 最新访问量
            latest_viewnum = PopRecord.objects.filter(
                pid=OuterRef('id')
            ).order_by('-recordtime').values('viewnum')[:1]

            # 话题最新访问量
            topic_latest_viewnum = Post.objects.filter(
                class_id=topic_id
            ).annotate(
                latest_views=Subquery(latest_viewnum),
            ).values('latest_views')

            # 话题总访问量
            topic_views = topic_latest_viewnum.aggregate(total_views=Sum('latest_views'))

            # 话题详情
            topic = Class.objects.get(class_id=topic_id)
            response_data = {
                'topic': topic.class_title,
                'content': topic.summary,
                'hotValue': topic.hot_value,
                'warnValue': 0,
                'visits': topic_views['total_views']
            }
            return JsonResponse(response_data, safe=False)
        except Exception as e:
            # 返回错误
            return JsonResponse({'error': e})
    else:
        # 返回400 Bad Request响应
        return JsonResponse({'error': 'Missing topicID'}, status=400)
    
#话题页接口2  
@require_http_methods(["GET"])
def get_topic_comments_stats(request):
    # 获取请求参数中的id
    topic_id = request.GET.get('topicID', None)
    
    # 检查id是否有效
    try:
        topic_id = int(topic_id)
    except (TypeError, ValueError):
        return HttpResponseBadRequest("Invalid topic ID format.")
    
    # 检查topic_id是否存在于post表的class_id字段中
    if not Post.objects.filter(class_id=topic_id).exists():
        return HttpResponseBadRequest("Topic ID does not exist.")
    
    # 提取post表中所有class_id符合传入id的记录
    posts = Post.objects.filter(class_id=topic_id).values('id')
    
    # 提取comments表中所有符合条件的数据的sentiment字段
    post_ids = [post['id'] for post in posts]
    comments = Comments.objects.filter(pid__in=post_ids).values('sentiment')
    
    # 转换为DataFrame
    comments_df = pd.DataFrame(comments)
    
    if comments_df.empty:
        return JsonResponse({"data": []})
    
    # 删除或置零极端的sentiment值
    comments_df['sentiment'] = comments_df['sentiment'].apply(lambda x: 0 if x > 0.9 or x < -0.95 else x)
    
    # 根据分类规则对sentiment数据进行分类
    def classify_sentiment(sentiment):
        if sentiment < -0.7:
            return 1
        elif -0.7 <= sentiment < -0.2:
            return 2
        elif -0.2 <= sentiment < 0.25:
            return 3
        else:
            return 4
    
    comments_df['category'] = comments_df['sentiment'].apply(classify_sentiment)
    
    # 统计各类别的数量
    category_counts = comments_df['category'].value_counts().sort_index().to_dict()
    
    # 构建返回的数据格式
    response_data = {
        "data": [
            {"name": "负面", "value": category_counts.get(1, 0)},
            {"name": "较负面", "value": category_counts.get(2, 0)},
            {"name": "普通", "value": category_counts.get(3, 0)},
            {"name": "正常", "value": category_counts.get(4, 0)},
        ]
    }
    
    return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})


# 获取评论舆论等级
# @require_http_methods(["GET"])  # 限制只能使用 GET 方法访问这个视图
# def get_topic(request):
#     try:
#         topic_id = int(request.GET.get('id', ''))
#     except ValueError:
#         # 返回400 Bad Request响应
#         return JsonResponse({'error': 'Invalid id format'}, status=400)
#     if topic_id:
#         try:
#             class_query_set = Class.objects.all().values(
#                 'data',
#                 'visit',
#             )
#             class_list = [
#                 {
#                     'name': item['name'],
#                     'visit': item['visit']
#                 }
#                 for item in class_query_set
#             ]
#             response_data = {
#                 "data": class_list,
#             }
#             return JsonResponse(data, safe=False)
#         except Exception as e:
#             # 返回错误
#             return JsonResponse({'error': e})
#     else:
#         # 返回400 Bad Request响应
#         return JsonResponse({'error': 'Missing topicID'}, status=400)


# 获取话题近5日浏览量
@require_http_methods(["GET"])  # 限制只能使用 GET 方法访问这个视图
def get_topic_5days(request):
    try:
        topic_id = int(request.GET.get('topicID', ''))
    except ValueError:
        # 返回400 Bad Request响应
        return JsonResponse({'error': 'Invalid id format'}, status=400)
    if topic_id:
        try:
            # post 索引
            post_ids = Post.objects.filter(class_id=topic_id).values_list('id', flat=True)

            # 根据日期排序的 topic 每日访问量
            topic_date_views = PopRecord.objects.filter(
                pid__in=post_ids  # 使用 __in 查找与 post ids 匹配的记录
            ).annotate(
                date=TruncDate('recordtime')
            ).values(
                'date'
            ).annotate(
                total_views=Sum('viewnum')
            ).order_by('date')  # 根据日期排序

            data_views_list = [
                {'date': record['date'].strftime('%m-%d'),
                 'visit': record['total_views']
                 } for record in topic_date_views]

            response_data = {
                'data': data_views_list
            }
            return JsonResponse(response_data, safe=False)
        except Exception as e:
            # 返回错误
            return JsonResponse({'error': e})
    else:
        # 返回400 Bad Request响应
        return JsonResponse({'error': 'Missing topicID'}, status=400)


# 获取话题内帖子热度榜单
@require_http_methods(["GET"])  # 限制只能使用 GET 方法访问这个视图
def get_topic_postlist(request):
    try:
        topic_id = int(request.GET.get('topicID', ''))
    except ValueError:
        # 返回400 Bad Request响应
        return JsonResponse({'error': 'Invalid id format'}, status=400)
    if topic_id:
        try:
            # post 热度
            hot_value = PopRecord.objects.filter(
                pid=OuterRef('id')
            ).values('hotval')[:1]

            # post
            post_query = Post.objects.filter(class_id=topic_id).annotate(
                hot_value=Subquery(hot_value)
            ).values(
                'title',
                'hot_value'
            ).order_by('-hot_value')

            post_list = [
                {
                    'class': '一类',
                    'platform': '校园集市',
                    'post': item['title'],
                    'value': item['hot_value']
                }
                for item in post_query
            ]
            print(post_list)
            response_data = {
                "data": post_list,
            }
            return JsonResponse(response_data)
        except Exception as e:
            # 返回错误
            return JsonResponse({'error': e})
    else:
        # 返回400 Bad Request响应
        return JsonResponse({'error': 'Missing topicID'}, status=400)
