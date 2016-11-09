from django.conf.urls import url
from .views import timeline, demo

urlpatterns = [
    url(r'^$', demo, name='timeline_demo'),
    url(r'^timeline$', timeline, name='timeline'),
]
