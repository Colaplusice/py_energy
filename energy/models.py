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
    type=models.ForeignKey(Type, to_field=Type.name)
    content=models.TextField()
    title=models.CharField(max_length=128)
    img=models.FileField(default='')
    def __str__(self):
        return self.type+'--'+self.title







