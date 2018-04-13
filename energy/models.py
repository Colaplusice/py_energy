# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as timezone

# Create your models here.

class Type(models.Model):
    name = models.CharField(max_length=128,unique=True)

    def __str__(self):
        return  self.name


class Message(models.Model):
    user=models.ForeignKey(User,default=1)
    pub_date=models.DateTimeField(default=timezone.now)
    type=models.ForeignKey(Type)
    content=models.TextField()
    title=models.CharField(max_length=128)
    views=models.IntegerField(default=0)
    img=models.FileField(null=True,blank=True)
    is_deal=models.BooleanField(default=False)

    def __str__(self):
        return  self.title

class Commit(models.Model):
    user = models.ForeignKey(User, default=1)
    pub_date = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    message = models.ForeignKey(Message)

    def __str__(self):
        return  self.content


class Article(models.Model):
    user=models.ForeignKey(User,default=1)
    content=models.TextField()
    pub_date=models.DateTimeField(default=timezone.now)
    title=models.CharField(max_length=128)
    views=models.IntegerField(default=0)
    type=models.ForeignKey(Type)
    def __str__(self):
        return  self.title


#文章类的子表 文章的图片
class ArticleImg(models.Model):
        article=models.ForeignKey(Article)
        img=models.FileField()


