# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-12 09:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0013_auto_20160911_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='sina_id',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name=b'\xe5\xbe\xae\xe5\x8d\x9aID'),
        ),
        migrations.AlterField(
            model_name='account',
            name='biography',
            field=models.TextField(blank=True, null=True, verbose_name=b'\xe7\xae\x80\xe4\xbb\x8b'),
        ),
        migrations.AlterField(
            model_name='account',
            name='display_name',
            field=models.CharField(max_length=128, verbose_name=b'\xe6\x98\xb5\xe7\xa7\xb0'),
        ),
        migrations.AlterField(
            model_name='account',
            name='homepage',
            field=models.URLField(blank=True, null=True, verbose_name=b'\xe4\xb8\xbb\xe9\xa1\xb5'),
        ),
        migrations.AlterField(
            model_name='account',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7'),
        ),
        migrations.AlterField(
            model_name='account',
            name='weibo',
            field=models.URLField(blank=True, null=True, verbose_name=b'\xe5\xbe\xae\xe5\x8d\x9a'),
        ),
        migrations.AlterField(
            model_name='article',
            name='abstract',
            field=models.CharField(blank=True, help_text=b'\xe5\x8f\xaf\xe9\x80\x89,\xe8\x8b\xa5\xe4\xb8\xba\xe7\xa9\xba\xe5\x88\x99\xe5\x8f\x96\xe6\x96\x87\xe7\xab\xa0\xe5\x89\x8d54\xe4\xb8\xaa\xe5\xad\x97\xe7\xac\xa6', max_length=54, null=True, verbose_name=b'\xe6\x91\x98\xe8\xa6\x81'),
        ),
        migrations.AlterField(
            model_name='article',
            name='body',
            field=models.TextField(verbose_name=b'\xe6\xad\xa3\xe6\x96\x87'),
        ),
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='article.Category', verbose_name=b'\xe7\xb1\xbb\xe5\x90\x8d'),
        ),
        migrations.AlterField(
            model_name='article',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='article',
            name='last_modified_time',
            field=models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='article',
            name='likes',
            field=models.PositiveIntegerField(default=0, verbose_name=b'\xe7\x82\xb9\xe8\xb5\x9e\xe6\x95\xb0'),
        ),
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(choices=[(b'd', b'Draft'), (b'p', b'Published')], default=b'd', max_length=1, verbose_name=b'\xe6\x96\x87\xe7\xab\xa0\xe7\x8a\xb6\xe6\x80\x81'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(blank=True, to='article.Tag', verbose_name=b'\xe6\xa0\x87\xe7\xad\xbe\xe9\x9b\x86\xe5\x90\x88'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=70, verbose_name=b'\xe6\xa0\x87\xe9\xa2\x98'),
        ),
        migrations.AlterField(
            model_name='article',
            name='topped',
            field=models.BooleanField(default=False, verbose_name=b'\xe7\xbd\xae\xe9\xa1\xb6'),
        ),
        migrations.AlterField(
            model_name='article',
            name='views',
            field=models.PositiveIntegerField(default=0, verbose_name=b'\xe6\xb5\x8f\xe8\xa7\x88\xe9\x87\x8f'),
        ),
        migrations.AlterField(
            model_name='category',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='category',
            name='last_modified_time',
            field=models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=20, verbose_name=b'\xe7\xb1\xbb\xe5\x90\x8d'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='article.Article', verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe6\x89\x80\xe5\xb1\x9e\xe6\x96\x87\xe7\xab\xa0'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe5\x86\x85\xe5\xae\xb9'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe5\x8f\x91\xe8\xa1\xa8\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='article.Account', verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='last_modified_time',
            field=models.DateTimeField(auto_now=True, verbose_name=b'\xe4\xbf\xae\xe6\x94\xb9\xe6\x97\xb6\xe9\x97\xb4'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=20, verbose_name=b'\xe6\xa0\x87\xe7\xad\xbe\xe5\x90\x8d'),
        ),
    ]