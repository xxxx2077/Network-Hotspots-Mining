from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse

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