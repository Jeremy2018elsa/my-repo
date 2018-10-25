from django.conf.urls import url
from .views import *
urlpatterns = [
    #访问路径是 /
    url(r'^$',index_views),
    #访问路径是 /login
    url(r'^login/$',login_views),
    #访问路径是 /register
    url(r'^register/$',register_views),
    url(r'^checkphone/$',checkphone_views),
    url(r'^checkLogin/$',checkLogin_views),
    url(r'^logout/$',logout_views),
    url(r'^loadgoods/$',loadgoods_views),
    url(r'^addcart/$',addcart_views),
    url(r'^cartcount/$',cartcount_views),
]







