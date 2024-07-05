from django.db.models import F, OuterRef, Subquery, Sum
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


# 获取热榜
@require_http_methods(["GET"])
def get_hotlist(request):
    try:
        class_query_set = Class.objects.all().values(
            'class_id',
            'class_title',
            'summary',
            'hot_value'
        ).order_by('-hot_value')
        class_list = [
            {
                'id': item['class_id'],
                'class': item['class_title'],
                'topic': item['summary'],
                'value': item['hot_value']
            }
            for item in class_query_set
        ]
        response_data = {
            "data": class_list,
        }
        return JsonResponse(response_data)
    except Exception as e:
        # 返回错误
        return JsonResponse({'error': e})


# 获取热度上升榜
@require_http_methods(["GET"])
def get_speedlist(request):
    try:
        class_query_set = Class.objects.all().values(
            'class_id',
            'class_title',
            'summary',
            'hot_value_perday'
        ).order_by('-hot_value_perday')
        class_list = [
            {
                'id': item['class_id'],
                'class': item['class_title'],
                'topic': item['summary'],
                'value': item['hot_value_perday']
            }
            for item in class_query_set
        ]
        response_data = {
            "data": class_list,
        }
        return JsonResponse(response_data)
    except Exception as e:
        # 返回错误
        return JsonResponse({'error': e})


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

            # 话题访问量
            post = Post.objects.filter(
                class_id=OuterRef('class_id')
            ).annotate(
                latest_views = Subquery(latest_viewnum),
                total_views = Sum('latest_views')
            ).values('total_views')

            # 话题详情
            topic = Class.objects.filter(class_id=topic_id).annotate(
                total_views=Subquery(post)
            ).values(
                'class_title',
                'summary',
                'hot_value',
                'total_views'
            )
            response_data = {
                'topic': topic[0]['class_title'],
                # 'content': topic[0].summary,
                # 'hotValue': topic[0].hot_value,
                # 'warnValue': 0,
                # 'visits': topic[0].total_views
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
