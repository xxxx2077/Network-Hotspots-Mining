from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from app.controller.single_pass import launch_single_pass,get_event_list
from app.controller.LLM import LLM_summary, LLM_class
from app.models import Comments,Post
from app.util.util import querySet_to_list
from app.misc.test import preprocess_data
import concurrent.futures
import os
# Create your views here.
def hello_str(request):
    return HttpResponse('Hello,world!')

def hello_json(request):
    dic ={
        'name':'时代少年团',
        'content':'我们喜欢你'
    }
    return JsonResponse(dic)

def bilibili(request):
    return redirect('https://www.bilibili.com')

def testdb(request):
    response = ''
    response1 = ''
    listTest = Comments.objects.all()
    for var in listTest:
        response1 += var.content + " "
    response = response1
    return HttpResponse("<p>" + response + "</p>")

def test_data(request):
    preprocess_data()
    return HttpResponse('get_data done')

def LLM_summary_db(request):
    # print('LLM_summary_db is running...')
    # with concurrent.futures.ThreadPoolExecutor() as executor:      
    #     id_querySet = Post.objects.values('id').all()
    #     id_list = querySet_to_list(id_querySet,'id')
    #     print(id_list)
    #     for post_id in id_list:
    #         executor.submit(LLM_summary, post_id)
    #     print('wait for result...')
    #     executor.shutdown
    # print('LLM_summary_db done!')

    print('LLM_summary_db is running...')
    with concurrent.futures.ThreadPoolExecutor() as executor:      
        id_querySet = Post.objects.values('id').all()
        id_list = querySet_to_list(id_querySet,'id')
        print(id_list)
        print('wait for result...')
        result = executor.map(LLM_summary, id_list)
        with open(os.path.join(os.path.dirname(__file__),"result/LLM_summary_db_res.txt"), "w", encoding="utf-8") as f:
            for res in result:
                res = res+'\n'
                print(res)
                f.write(res)
        
    print('LLM_summary_db done!')

def LLM(request):
    # LLM_summary(post_id=1813553090)
    # print('summary done!')

    launch_single_pass()
    print('text_cluster done!')

    LLM_class()
    print('text_cluster_catorizing done!')

    return HttpResponse('success!')
