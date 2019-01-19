from __future__ import unicode_literals

from django.contrib import admin
from energy.models import Message, Type, Commit, Article

# register your models here.
admin.site.register(Message)
admin.site.register(Type)
admin.site.register(Commit)
admin.site.register(Article)
