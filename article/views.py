from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.contrib.auth.hashers import make_password,check_password
from django.db.models import Q
from .models import Article,Category,Tag,User
from .forms import CommentForm,RegisterForm,LoginForm

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
        kwargs['category_list']=Category.objects.all().order_by('name')
        kwargs['tag_list']=Tag.objects.all().order_by('name')
        kwargs['date_archive']=Article.objects.archive()
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
        kwargs['category_list']=Category.objects.all().order_by('name')
        kwargs['tag_list']=Tag.objects.all().order_by('name')
        kwargs['date_archive']=Article.objects.archive()
        return super(CommentView,self).get_context_data(**kwargs)

class SearchView(ListView):
    template_name = 'article/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        if 's' in self.request.GET:
            s=self.request.GET['s']
            if s:
                article_list=Article.objects.filter(Q(title__contains=s)|Q(category__name__contains=s)|Q(tag__name__contains=s)
                |Q(body__contains=s)|Q(comment__body__contains=s),Q(status='p'))
                article_list=list(set(article_list))
                return article_list

        article_list=Article.objects.filter(status='p')
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list']=Category.objects.all().order_by('name')
        kwargs['tag_list']=Tag.objects.all().order_by('name')
        kwargs['date_archive']=Article.objects.archive()
        if 's' in self.request.GET:
            kwargs['search']=True
            kwargs['s']=self.request.GET['s']
        return super(SearchView,self).get_context_data(**kwargs)

class RSSFeed(Feed):
    title='blog article'
    link='/latest/feed/'
    description='the six latest articles of the blog'

    def items(self):
        return Article.objects.order_by('-last_modified_time')[:6]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_pubdate(self,item):
        return item.last_modified_time

class RegisterView(FormView):
    template_name = 'article/user.html'
    form_class = RegisterForm

    def form_valid(self, form):
        user=form.save(commit=False)
        user.password=make_password(user.password)
        user.save()
        return render(self.request,'article/user_ok.html',{'register':True})

    def form_invalid(self, form):
        return render(self.request, 'article/user.html', {'form':form,'register':True})

    def get_context_data(self, **kwargs):
        kwargs['register']=True
        kwargs['category_list']=Category.objects.all().order_by('name')
        kwargs['tag_list']=Tag.objects.all().order_by('name')
        kwargs['date_archive']=Article.objects.archive()
        return super(RegisterView,self).get_context_data(**kwargs)

class LoginView(FormView):
    template_name = 'article/user.html'
    form_class = LoginForm

    def form_valid(self, form):
        user=User.objects.filter(Q(user_name=self.request.POST['user_name'])|Q(user_email=self.request.POST['user_name']))
        if user and check_password(self.request.POST['password'],user[0].password):
            user.update(user_status='y')
            return render(self.request, 'article/user_ok.html',{'login':True})
        else:
            return render(self.request, 'article/user.html', {'form':form,'login':True})

    def form_invalid(self, form):
        return render(self.request, 'article/user.html', {'form':form,'login':True})

    def get_context_data(self, **kwargs):
        kwargs['login']=True
        kwargs['category_list']=Category.objects.all().order_by('name')
        kwargs['tag_list']=Tag.objects.all().order_by('name')
        kwargs['date_archive']=Article.objects.archive()
        return super(LoginView,self).get_context_data(**kwargs)

def test(request):
    return render(request,'article/test.html')