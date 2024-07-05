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
import os
import json

from django.views.decorators.http import require_http_methods


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


# 获取热榜
@require_http_methods(["GET"])
def get_hotlist(request):
    # 获取满足条件的前十条记录，按 hot_value 从高到低排序
    class_querySet = Class.objects.filter(hot_value__gte=200).order_by('-hot_value')[:10]

    # 构建返回的数据
    response_data = {
        "data": [
            {
                "id": cls.class_id,
                "class": "负面事件",
                "topic": cls.class_title,
                "value": cls.hot_value
            } for cls in class_querySet
        ]
    }

    if len(class_querySet) == 10:
        # 尝试获取更多热度大于x值的记录
        additional_querySet = Class.objects.filter(hot_value__gte=200).exclude(
            pk__in=[cls.pk for cls in class_querySet])
        for cls in additional_querySet:
            response_data["data"].append({
                "id": cls.class_id,
                "class": "负面事件",
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
        "data": [
            {
                "id": cls.class_id,
                "class": "负面事件",
                "topic": cls.class_title,
                "value": cls.hot_value_perday
            } for cls in class_querySet
        ]
    }

    if len(class_querySet) == 10:
        # 尝试获取更多热度大于x值的记录
        additional_querySet = Class.objects.filter(hot_value_perday__gte=100).exclude(
            pk__in=[cls.pk for cls in class_querySet])
        for cls in additional_querySet:
            response_data["data"].append({
                "id": cls.class_id,
                "class": "负面事件",
                "topic": cls.class_title,
                "value": cls.hot_value_perday
            })

    return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})


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
