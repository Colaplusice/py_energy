from django.conf.urls import url
from django.contrib import admin
from . import views
app_name='energy'
urlpatterns = [
    url(r'^index',views.index,name='index'),
    url(r'^submit_msg',views.submit_msg,name='submit_msg'),
    url(r'^Login',views.Login,name='Login'),
    url(r'^Logout',views.Logout,name='Logout'),
    url(r'^Forum',views.Forum,name='forum'),
    url(r'^Register',views.Register,name='register'),
    url(r'^detail',views.detail,name='detail'),
]
