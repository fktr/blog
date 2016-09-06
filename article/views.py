from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Article,Category

# Create your views here.
class IndexView(ListView):
    template_name = 'article/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        article_list=Article.objects.filter(status='p')
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list']=Category.objects.all().order_by('name')
        return super(IndexView,self).get_context_data(**kwargs)

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article/detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'article_id'

    def get_object(self, queryset=None):
        article=super(ArticleDetailView,self).get_object()
        return article

class CategoryView(ListView):
    template_name = 'article/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        article_list=Article.objects.filter(category=self.kwargs['category_id'],status='p')
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list']=Category.objects.all().order_by('name')
        return super(CategoryView,self).get_context_data(**kwargs)
