# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-24 02:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('energy', '0009_message_is_deal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=128)),
                ('views', models.IntegerField(default=0)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='energy.Type')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleImg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.FileField(upload_to=b'')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='energy.Article')),
            ],
        ),
        migrations.AlterField(
            model_name='message',
            name='img',
            field=models.FileField(blank=True, null=True, upload_to=b''),
        ),
    ]