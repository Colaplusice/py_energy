from django.conf.urls import url

from . import views

app_name = "energy"

urlpatterns = [
    url(r"^index", views.index, name="index"),
    url(r"^submit_msg", views.submit_msg, name="submit_msg"),
    url(r"^login", views.login, name="login"),
    url(r"^log_out", views.log_out, name="log_out"),
    url(r"^forum", views.forum, name="forum"),
    url(r"^register", views.register, name="register"),
    url(r"^sendmail", views.sendmail, name="sendmail"),
    url(r"^article", views.articles, name="article"),
    url(r"^blog/(?P<blog_id>[0-9])/$", views.blog, name="blog"),
    url(r"^detail/(?P<message_id>[0-9])/$", views.detail, name="detail"),
    url(r"^verify", views.verify, name="verify"),
    url(r"^yz_home", views.yz_home, name="yz_home"),
    url(r"^test_1", views.test_1, name="test_1"),
]
# +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT),
