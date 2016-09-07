from django import forms
from .models import Comment,User

class CommentForm(forms.ModelForm):

    class Meta:
        model=Comment
        fields=['user_name','user_email','body']
        widgets={
            'user_name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'请输入昵称',
            }),
            'user_email':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'请输入邮箱',
            }),
            'body':forms.Textarea(attrs={
                'placeholder':'我来评论两句~',
            })
        }

class RegisterForm(forms.ModelForm):

    class Meta:
        model=User
        fields=['user_name','password','user_email']
        widgets={
            'user_name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'请输入你的用户名称',
            }),
            'password':forms.PasswordInput(attrs={
                'class':'form-control',
                'placeholder':'请输入你的密码',
            }),
            'user_email':forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder':'请输入你的邮箱',
            }),
        }

class LoginForm(forms.ModelForm):

    class Meta:
        model=User
        fields=['user_name','password']
        widgets={
            'user_name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'请输入你的昵称或邮箱',
            }),
            'password':forms.PasswordInput(attrs={
                'class':'form-control',
                'placeholder':'请输入你的密码',
            }),
        }

