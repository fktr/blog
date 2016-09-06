from django import forms
from .models import Comment

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
