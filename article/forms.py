# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate

class CommentForm(forms.Form):
    body=forms.CharField(max_length=1024,widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'我来评论两句~'
    }))

class RegisterForm(forms.Form):
    username=forms.CharField(label='用户名', max_length=256,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'请输入用户名'
    }))
    email=forms.EmailField(label='邮箱',max_length=256,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'请输入邮箱'
    }))
    password=forms.CharField(label='密码',max_length=256,widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'请输入密码'
    }))
    password_confirm=forms.CharField(label='重复密码',max_length=256,widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'请确认密码'
    }))

    def clean(self):
        cleaned_data=super(RegisterForm,self).clean()
        password=cleaned_data['password']
        password_confirm=cleaned_data['password_confirm']
        if password!=password_confirm:
            raise forms.ValidationError('两次输入的密码不相同')

class LoginForm(forms.Form):
    username=forms.CharField(label='用户名',max_length=256,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'请输入用户名',
    }))
    password=forms.CharField(label='密码',max_length=256,widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'请输入密码'
    }))

class ProfileForm(forms.Form):
    display_name=forms.CharField(label='昵称',max_length=128,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'快来给自己起个好听的昵称吧~',
    }))
    biography=forms.CharField(required=False,label='简介',widget=forms.Textarea(attrs={
        'class':'form-control',
        'placeholder':'写点什么让别人了解你~',
    }))
    homepage=forms.URLField(required=False,label='主页',widget=forms.URLInput(attrs={
        'class':'form-control',
        'placeholder':'www.example.com'
    }))
    weibo=forms.URLField(required=False,label='微博',widget=forms.URLInput(attrs={
        'class':'form-control',
        'placeholder':'example.com'
    }))
    sina_id=forms.CharField(required=False,label='',max_length=128,widget=forms.HiddenInput)
    github=forms.URLField(required=False,label='GitHub',widget=forms.URLInput(attrs={
        'class':'form-control',
        'placeholder':'github.com/example'
    }))

class ChangePasswordForm(forms.Form):
    username=forms.CharField(label='用户名',max_length=256,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'请输入用户名'
    }))
    old_password=forms.CharField(label='旧密码',max_length=256,widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'请输入原来的密码',
    }))
    new_password=forms.CharField(label='新密码',max_length=256,widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'请输入新密码',
    }))
    confirm_password=forms.CharField(label='重复密码',max_length=256,widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'请确认密码',
    }))

    def clean(self):
        cleaned_data=super(ChangePasswordForm,self).clean()
        username=cleaned_data['username']
        password=cleaned_data['old_password']
        user=authenticate(username=username,password=password)
        if user is None:
            raise forms.ValidationError('用户名和密码不匹配')
        new_password=cleaned_data['new_password']
        confirm_password=cleaned_data['confirm_password']
        if new_password!=confirm_password:
            raise forms.ValidationError('两次输入的密码不相同')
