from django.contrib import admin
from .models import Article,Category,Tag,Comment,Account

# Register your models here.
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Account)
