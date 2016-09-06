from django.conf.urls import url
from .views import *

urlpatterns=[
    url(r'^$',IndexView.as_view(),name='index'),
    url(r'^article/(?P<article_id>\d+)/$',ArticleDetailView.as_view(),name='detail'),
    url(r'^category/(?P<category_id>\d+)/$',CategoryView.as_view(),name='category'),
    url(r'^tag/(?P<tag_id>\d+)/$',TagView.as_view(),name='tag'),

]