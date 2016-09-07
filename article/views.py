from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from itertools import  chain
from .models import Article,Category,Tag
from .forms import CommentForm

# Create your views here.
class IndexView(ListView):
    template_name = 'article/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        article_list=Article.objects.filter(status='p')
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list']=Category.objects.all().order_by('name')
        kwargs['tag_list']=Tag.objects.all().order_by('name')
        kwargs['date_archive']=Article.objects.archive()
        return super(IndexView,self).get_context_data(**kwargs)

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article/detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'article_id'

    def get_object(self, queryset=None):
        article=super(ArticleDetailView,self).get_object()
        return article

    def get_context_data(self, **kwargs):
        kwargs['comment_list']=self.object.comment_set.all()
        kwargs['form']=CommentForm()
        return super(ArticleDetailView,self).get_context_data(**kwargs)

class CategoryView(ListView):
    template_name = 'article/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        article_list=Article.objects.filter(category=self.kwargs['category_id'],status='p')
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list']=Category.objects.all().order_by('name')
        kwargs['tag_list']=Tag.objects.all().order_by('name')
        kwargs['date_archive']=Article.objects.archive()
        return super(CategoryView,self).get_context_data(**kwargs)

class TagView(ListView):
    template_name = 'article/index.html'
    content_type ='article_list'

    def get_queryset(self):
        article_list=Article.objects.filter(tag=self.kwargs['tag_id'],status='p')
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['tag_list']=Tag.objects.all().order_by('name')
        kwargs['category_list']=Category.objects.all().order_by('name')
        kwargs['date_archive']=Article.objects.archive()
        return super(TagView,self).get_context_data(**kwargs)

class ArchiveView(ListView):
    template_name = 'article/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        article_list=Article.objects.filter(created_time__month=self.kwargs['month'],created_time__day=self.kwargs['day'],status='p')
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list']=Category.objects.all().order_by('name')
        kwargs['tag_list']=Tag.objects.all().order_by('name')
        kwargs['date_archive']=Article.objects.archive()
        return super(ArchiveView,self).get_context_data(**kwargs)

class CommentView(FormView):
    template_name = 'article/detail.html'
    form_class = CommentForm

    def form_valid(self, form):
        target_article=get_object_or_404(Article,pk=self.kwargs['article_id'])
        comment=form.save(commit=False)
        comment.article=target_article
        comment.save()
        success_url=target_article.get_absolute_url()
        return HttpResponseRedirect(success_url)

    def form_invalid(self, form):
        target_article=get_object_or_404(Article,pk=self.kwargs['article_id'])
        return render(self.request,'article/detail.html',{'form':form,'article':target_article,'commnet_list':target_article.comment_set.all()})

    def get_context_data(self, **kwargs):
        target_article=get_object_or_404(Article,pk=self.kwargs['article_id'])
        kwargs['article']=target_article
        kwargs['form']=CommentForm()
        kwargs['comment_list']=target_article.comment_set.all()
        return super(CommentView,self).get_context_data(**kwargs)

class SearchView(ListView):
    template_name = 'article/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        if 's' in self.request.GET:
            s=self.request.GET['s']
            if s:
                search_title=Article.objects.filter(title__contains=s,status='p')
                search_category=Article.objects.filter(category__name__contains=s,status='p')
                search_tag=Article.objects.filter(tag__name__contains=s,status='p')
                search_content=Article.objects.filter(body__contains=s,status='p')
                search_comment=Article.objects.filter(comment__body__contains=s,status='p')
                article_list=list(set(chain(search_title,search_category,search_tag,search_content,search_comment)))
                return article_list

        article_list=Article.objects.filter(status='p')
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list']=Category.objects.all().order_by('name')
        kwargs['tag_list']=Tag.objects.all().order_by('name')
        kwargs['date_archive']=Article.objects.archive()
        kwargs['search']=True
        kwargs['s']=self.request.GET['s']
        return super(SearchView,self).get_context_data(**kwargs)

