from django.views.generic import ListView,DetailView,View
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Article,Category,Tag,Comment,Account
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
        article_list=Article.objects.filter(created_time__month=self.kwargs['month'],
                                            created_time__day=self.kwargs['day'],status='p')
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list']=Category.objects.all().order_by('name')
        kwargs['tag_list']=Tag.objects.all().order_by('name')
        kwargs['date_archive']=Article.objects.archive()
        return super(ArchiveView,self).get_context_data(**kwargs)

class CommentView(View):

    def get(self,request,article_id,form=None):
        if not form:
            form=CommentForm(request.GET)
        article=get_object_or_404(Article,pk=article_id)
        comment_list=article.comment_set.all()
        category_list=Category.objects.all().order_by('name')
        tag_list=Tag.objects.all().order_by('name')
        date_archive=Article.objects.archive()
        data={'article':article,'form':form,'comment_list':comment_list,'category_list':category_list,
              'tag_list':tag_list,'date_archive':date_archive}
        return render(request,'article/detail.html',data)

    def post(self,request,article_id):
        form=CommentForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated():
                article=get_object_or_404(Article,pk=article_id)
                body=form.cleaned_data['body']
                user=Account.objects.get(user=request.user)
                comment=Comment.objects.create(body=body,article=article,user=user)
                comment.save()
                msg='评论成功'
                messages.add_message(request,messages.SUCCESS,msg)
                url=article.get_absolute_url()
                return redirect(url)
            else:
                msg='登录之后才能发言哦'
                messages.add_message(request,messages.WARNING,msg)
                return self.get(request,article_id,form)
        else:
            return self.get(request,article_id,form)

class SearchView(ListView):
    template_name = 'article/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        if 's' in self.request.GET:
            s=self.request.GET['s']
            if s:
                article_list=Article.objects.filter(Q(title__contains=s)|Q(category__name__contains=s)
                |Q(tag__name__contains=s)|Q(body__contains=s)|Q(comment__body__contains=s),Q(status='p'))
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

class RegisterView(View):

    def get(self,request,form=None):
        if not form:
            form=RegisterForm(request.GET)
        data={'form':form,'btn_name':'注册'}
        return render(request,'article/simple_form.html',data)

    def post(self,request):
        form=RegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            email=form.cleaned_data['email']
            user=User.objects.create_user(username,email,password)
            user.save()
            msg='注册成功'
            messages.add_message(request,messages.SUCCESS,msg)
            url=reverse('article:login')
            return redirect(url)
        else:
            return self.get(request,form)

class LoginView(View):

    def get(self,request,form=None):
        if not form:
            form=LoginForm(request.GET)
        data={'form':form,'btn_name':'登录'}
        return render(request,'article/simple_form.html',data)

    def post(self,request):
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    url=request.GET.get('next')
                    if not url:
                        url=reverse('article:index')
                    return redirect(url)
                else:
                    msg='账户被禁用'
                    messages.add_message(request,messages.WARNING,msg)
                    return self.get(request,form)
            else:
                msg='登录无效,请重新尝试'
                messages.add_message(request,messages.ERROR,msg)
                return self.get(request,form)
        else:
            return self.get(request,form)

class LogoutView(View):

    def get(self,request):
        logout(request)
        url=reverse('article:login')
        return redirect(url)

def test(request):
    return render(request,'article/test.html')

