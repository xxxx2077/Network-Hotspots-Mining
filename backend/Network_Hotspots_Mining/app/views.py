from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from app.controller.single_pass import launch_single_pass, get_data
from app.controller.LLM import LLM_summary, LLM_class
from app.models import Comments, Post, Class
from app.util.util import querySet_to_list
from app.misc.data_processing import preprocess_data, mark_used, days_calculating
from app.misc.clear_db import clear_db_class, clear_db_summary
from app.misc.test import fuck
import concurrent.futures
import os
import json
from django.db.models import Q


# Create your views here.
def test(request):
    fuck()
    return HttpResponse('Hello,world!')


def preprocess(request):
    preprocess_data()
    return HttpResponse('get_data done')


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
    # launch_single_pass()
    LLM_class()

    return HttpResponse('text_cluster_catorizing done!')

#获取热榜
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
        additional_querySet = Class.objects.filter(hot_value__gte=200).exclude(pk__in=[cls.pk for cls in class_querySet])
        for cls in additional_querySet:
            response_data["data"].append({
                "id": cls.class_id,
                "class": "负面事件",
                "topic": cls.class_title,
                "value": cls.hot_value
            })
    
    return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})


#获取热度上升榜
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
        additional_querySet = Class.objects.filter(hot_value_perday__gte=100).exclude(pk__in=[cls.pk for cls in class_querySet])
        for cls in additional_querySet:
            response_data["data"].append({
                "id": cls.class_id,
                "class": "负面事件",
                "topic": cls.class_title,
                "value": cls.hot_value_perday
            })
    
    return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})



