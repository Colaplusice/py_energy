# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *

# Register your models here.
admin.site.register(Message)
admin.site.register(Type)
admin.site.register(Commit)
admin.site.register(Article)


