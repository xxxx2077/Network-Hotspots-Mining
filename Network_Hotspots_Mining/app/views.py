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
        id_list = id_list[:500]
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


def get_hotlist(request):
    class_querySet = Class.objects.all().values('class_title', 'summary', 'hot_value').order_by('hot_value').all()
    # hotlist_json = json.dumps(class_querySet, ensure_ascii=False)
    response_data = {
        "data": list(class_querySet),
    }
    return JsonResponse(response_data)


def get_speedlist(request):
    class_querySet = Class.objects.all().values('class_title', 'summary', 'hot_value_perday').order_by(
        'hot_value_perday').all()
    # speedlist_json = json.dumps(class_querySet, ensure_ascii=False)
    response_data = {
        "data": list(class_querySet),
    }
    return JsonResponse(response_data)
