"""
URL configuration for Network_Hotspots_Mining project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('test/',views.test),
    # path('preprocess/',views.preprocess),
    path('clear/',views.clear),
    path('LLM/',views.LLM),
    path('LLM_summary_db/',views.LLM_summary_db),

    # 主页
    path('hotlist',views.get_hotlist),
    path('speedlist',views.get_speedlist),
    path('classHotValue', views.get_weekly_event_hotval),

    # 话题详细页
    path('topic/details', views.get_topic_details),
    path('topic/5days', views.get_topic_5days),
    path('topic/postlist', views.get_topic_postlist)
]
