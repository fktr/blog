from django import forms
from .models import Comment,Account

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
            raise forms.ValidationError('Two password are not the same')

class LoginForm(forms.Form):
    username=forms.CharField(label='用户名',max_length=256,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'请输入用户名',
    }))
    password=forms.CharField(label='密码',max_length=256,widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'请输入密码'
    }))
