from celery import shared_task
from .models import Post
import concurrent.futures
from django.db.models import F
from app.controller.LLM import LLM_summary, LLM_class
from app.util.util import querySet_to_list


# 监听数据库消息，自动更新
@shared_task
def LLM_summary_db():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        id_querySet = Post.objects.filter(is_summaried=False).values('id').order_by('-time')[:100]
        if id_querySet.exists():
            id_list = querySet_to_list(id_querySet, 'id')
            result = executor.map(LLM_summary, id_list)
    return "Processed new posts."

