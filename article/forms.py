from django import forms
from .models import Comment,User

class CommentForm(forms.ModelForm):

    class Meta:
        model=Comment
        fields=['body']
        widgets={
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
                'placeholder':'请输入你的用户昵称',
            }),
            'password':forms.PasswordInput(attrs={
                'class':'form-control',
                'placeholder':'请输入你的密码',
            }),
            'user_email':forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder':'请输入你的验证邮箱',
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

