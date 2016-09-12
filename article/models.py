# -*- coding: utf-8 -*-
from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
import collections

# Create your models here.
class ArticleManager(models.Manager):

    def archive(self):
        date_list=Article.objects.datetimes('created_time','day','DESC')
        date_dict=collections.defaultdict(list)

        for d in date_list:
            date_dict[d.month].append(d.day)
        return sorted(date_dict.items(),reverse=True)

class Article(models.Model):
    STATUS_CHOICE=(
        ('d','Draft'),
        ('p','Published'),
    )

    objects=ArticleManager()
    title=models.CharField('标题',max_length=70)
    body=models.TextField('正文')
    created_time=models.DateTimeField('创建时间',auto_now_add=True)
    last_modified_time=models.DateTimeField('修改时间',auto_now=True)
    status=models.CharField('文章状态',max_length=1,choices=STATUS_CHOICE,default='d')
    abstract=models.CharField('摘要',max_length=54,blank=True,null=True,help_text='可选,若为空则取文章前54个字符')
    views=models.PositiveIntegerField('浏览量',default=0)
    likes=models.PositiveIntegerField('点赞数',default=0)
    topped=models.BooleanField('置顶',default=False)
    category=models.ForeignKey('Category',verbose_name='类名',null=True,on_delete=models.CASCADE)
    tag=models.ManyToManyField('Tag',verbose_name='标签集合',blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:detail', kwargs={'article_id':self.pk})

    class Meta:
        ordering=['-last_modified_time']

class Category(models.Model):
    name=models.CharField('类名',max_length=20)
    created_time=models.DateTimeField('创建时间',auto_now_add=True)
    last_modified_time=models.DateTimeField('修改时间',auto_now=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name=models.CharField('标签名',max_length=20)
    created_time=models.DateTimeField('创建时间',auto_now_add=True)
    last_modified_time=models.DateTimeField('修改时间',auto_now=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    user=models.ForeignKey('Account',verbose_name='用户',null=True,on_delete=models.CASCADE)
    body=models.TextField('评论内容')
    created_time=models.DateTimeField('评论发表时间',auto_now_add=True)
    article=models.ForeignKey('Article',verbose_name='评论所属文章',null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.body[:20]

    class Meta:
        ordering=['-created_time']

class Account(models.Model):
    user=models.OneToOneField(User,verbose_name='用户')
    display_name=models.CharField('昵称',max_length=128)
    biography=models.TextField('简介',null=True,blank=True)
    homepage=models.URLField('主页',null=True,blank=True)
    weibo=models.URLField('微博',null=True,blank=True)
    sina_id=models.CharField('微博ID',max_length=128,null=True,blank=True)
    github=models.URLField('GitHub',null=True,blank=True)

    @receiver(post_save,sender=User)
    def create_user_account(sender,instance=None,created=False,**kwargs):
        if created:
            Account.objects.get_or_create(user=instance,defaults={'display_name':instance.username})

    def __str__(self):
        return self.display_name
