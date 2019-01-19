from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as timezone


class Type(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.PROTECT)
    pub_date = models.DateTimeField(default=timezone.now)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    content = models.TextField()
    title = models.CharField(max_length=128)
    views = models.IntegerField(default=0)
    img = models.FileField(null=True, blank=True)
    is_deal = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Commit(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.PROTECT)
    pub_date = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    message = models.ForeignKey(Message, on_delete=models.PROTECT)

    def __str__(self):
        return self.content


class Article(models.Model):
    user = models.ForeignKey(User, default=1,on_delete=models.PROTECT)
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=128)
    views = models.IntegerField(default=0)
    type = models.ForeignKey(Type,on_delete=models.PROTECT)

    def __str__(self):
        return self.title


# 文章类的子表 文章的图片
class ArticleImg(models.Model):
    article = models.ForeignKey(Article, on_delete=models.PROTECT)
    img = models.FileField()
