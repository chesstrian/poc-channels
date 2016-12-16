from django.conf.urls import url

from chat import views

urlpatterns = [
    url('^$', views.user_login, name='user_login'),
    url('^logout/$', views.user_logout, name='user_logout'),
    url('^profile/$', views.profile, name='profile'),
    url('^chat/(?P<room>\d+)/$', views.chat, name='chat'),
    url('^history/(?P<room>\d+)/$', views.history, name='history')
]
