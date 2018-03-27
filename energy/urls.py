from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from . import views
app_name='energy'
urlpatterns = [
    url(r'^index',views.index,name='index'),
    url(r'^submit_msg',views.submit_msg,name='submit_msg'),
    url(r'^Login',views.Login,name='Login'),
    url(r'^Logout',views.Logout,name='Logout'),
    url(r'^Forum',views.Forum,name='forum'),
    url(r'^Register',views.Register,name='register'),
    url(r'^sendmail',views.sendmail,name='sendmail'),
    url(r'^article',views.Articles,name='article'),
    url(r'^blog/(?P<blog_id>[0-9])/$',views.Blog,name='blog'),
    url(r'^detail/(?P<Message_id>[0-9])/$',views.detail,name='detail'),
]
              # +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT),

