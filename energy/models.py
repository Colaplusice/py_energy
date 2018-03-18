# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Message(models.Model):
    user=models.ForeignKey(User,default=1)
    pub_date=models.DateTimeField()
    type=models.CharField(max_length=128)
    content=models.TextField()
    title=models.CharField(max_length=128)
    img=models.FileField(default='')
    def __str__(self):
        return self.type+'--'+self.title





