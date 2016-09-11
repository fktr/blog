from django.conf.urls import url
from .views import *

urlpatterns=[
    url(r'^$',IndexView.as_view(),name='index'),
    url(r'^article/(?P<article_id>\d+)/$',ArticleDetailView.as_view(),name='detail'),
    url(r'^category/(?P<category_id>\d+)/$',CategoryView.as_view(),name='category'),
    url(r'^tag/(?P<tag_id>\d+)/$',TagView.as_view(),name='tag'),
    url(r'^archive/(?P<month>\d+)/(?P<day>\d+)/$',ArchiveView.as_view(),name='archive'),
    url(r'^article/(?P<article_id>\d+)/comment/$',CommentView.as_view(),name='comment'),
    url(r'^search/$',SearchView.as_view(),name='search'),
    url(r'^latest/feed/$',RSSFeed(),name='rss'),
    url(r'^register/$',RegisterView.as_view(),name='register'),
    url(r'^activeuser/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$',active_user,name='activeuser'),
    url(r'^login/$',LoginView.as_view(),name='login'),
    url(r'^logout/$',LogoutView.as_view(),name='logout'),
    url(r'^profile/$',ProfileView.as_view(),name='profile'),
    url(r'^profile/password/$',ChangePasswordView.as_view(),name='change_password'),
    url(r'^test/$',test)
]
