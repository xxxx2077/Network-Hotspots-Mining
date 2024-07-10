from celery import shared_task
from .models import Post, PopRecord
import concurrent.futures
from django.db.models import F, OuterRef, Subquery
from app.controller.LLM import LLM_summary, LLM_class, LLM_relation
from app.util.util import querySet_to_list
from app.controller.single_pass import launch_single_pass


# 监听数据库消息，自动更新
@shared_task
def LLM_summary_db():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # post 热度
        hot_value = PopRecord.objects.filter(
            pid=OuterRef('id')
        ).values('hotval')[:1]

        id_querySet = Post.objects.filter(is_summaried=False).annotate(
            hot_value=Subquery(hot_value)
        ).values('id').order_by('-hot_value')[:200]

        if id_querySet.exists():
            id_list = querySet_to_list(id_querySet, 'id')
            result = executor.map(LLM_summary, id_list)

    print("----------------------------------------------------------"
          "总结完成"
          "----------------------------------------------------------")


def LLM_class_db():
    """ 聚类 """
    launch_single_pass()

    print("----------------------------------------------------------"
          "聚类完成"
          "----------------------------------------------------------")

    """ 类别总结 """
    LLM_class()

    print("----------------------------------------------------------"
          "类别总结完成"
          "----------------------------------------------------------")

    """ 事件关系 """
    LLM_relation()

    print("----------------------------------------------------------"
          "事件关系完成"
          "----------------------------------------------------------")

