# -*- coding: utf-8 -*-
from django.views.generic import ListView,DetailView,View
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.conf import settings
from weibo import APIClient
from .models import Article,Category,Tag,Comment,Account
from .signatures import token_confirm
from .forms import CommentForm,RegisterForm,LoginForm,ChangePasswordForm,ProfileForm

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
        if self.request.user.is_anonymous():
            kwargs['user']=False
        else:
            kwargs['user']=self.request.user.account.display_name
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
        if self.request.user.is_anonymous():
            kwargs['user']=False
        else:
            kwargs['user']=self.request.user.account.display_name
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
        if self.request.user.is_anonymous():
            kwargs['user']=False
        else:
            kwargs['user']=self.request.user.account.display_name
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
        if self.request.user.is_anonymous():
            kwargs['user']=False
        else:
            kwargs['user']=self.request.user.account.display_name
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
        if self.request.user.is_anonymous():
            kwargs['user']=False
        else:
            kwargs['user']=self.request.user.account.display_name
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
        if self.request.user.is_anonymous():
            data['user']=False
        else:
            data['user']=self.request.user.account.display_name
        return render(request,'article/detail.html',data)

    def post(self,request,article_id):
        form=CommentForm(request.POST)
        article = get_object_or_404(Article, pk=article_id)
        url = article.get_absolute_url()
        if form.is_valid():
            if request.user.is_authenticated():
                body=form.cleaned_data['body']
                user=Account.objects.get(user=request.user)
                comment=Comment.objects.create(body=body,article=article,user=user)
                comment.save()
                msg='评论成功'
                data={'message':msg,'url':url}
                return render(request,'message.html',data)
            else:
                msg='登录之后才能发言哦'
                data={'message':msg,'url':url}
                return render(request,'message.html',data)
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
        if self.request.user.is_anonymous():
            kwargs['user']=False
        else:
            kwargs['user']=self.request.user.account.display_name
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
            form=RegisterForm()
        data={'form':form,'btn_name':'注册'}
        return render(request, 'accounts/register.html', data)

    def post(self,request):
        form=RegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            email=form.cleaned_data['email']
            user=User.objects.create_user(username,email,password)
            user.is_active=False
            user.save()
            token=token_confirm.generate_validate_token(username)
            message='欢迎加入我的博客,请访问该链接完成用户验证:%s' % '/'.join([settings.DOMAIN,'activeuser',token])
            send_mail('注册用户验证信息',message,'1767831392@qq.com',[email],fail_silently=False)
            msg='请登录到注册邮箱中验证用户,有效期为一个小时'
            url=reverse('article:index')
            data={'message':msg,'url':url}
            return render(request, 'message.html', data)
        else:
            return self.get(request,form)

def active_user(request,token):
    try:
        username=token_confirm.confirm_validate_token(token)
    except:
        username=token_confirm.remove_validate_token(token)
        users=User.objects.filter(username=username)
        for user in users:
            user.delete()
        msg='对不起,验证链接已经过期,请重新注册'
        url=reverse('article:register')
        data={'message':msg,'url':url}
        return render(request, 'message.html', data)
    try:
        user=User.objects.get(username=username)
    except User.DoesNotExist:
        msg='对不起,你所验证的用户不存在,请重新注册'
        url=reverse('article:register')
        data={'message':msg,'url':url}
        return render(request, 'message.html', data)
    user.is_active=True
    user.save()
    msg='验证成功'
    url=reverse('article:login')
    data={'message':msg,'url':url}
    return render(request, 'message.html', data)

class LoginView(View):

    def get(self,request,form=None):
        if not form:
            form=LoginForm()
        data={'form':form,'btn_name':'登录'}
        return render(request, 'accounts/login.html', data)

    def post(self,request):
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    msg='登陆成功'
                    url=reverse('article:index')
                    data={'message':msg,'url':url}
                    return render(request,'message.html',data)
                else:
                    msg='账户没有激活'
                    url=reverse('article:index')
                    data={'message':msg,'url':url}
                    return render(request,'message.html',data)
            else:
                msg='登录无效,请重新尝试'
                url=reverse('article:login')
                data={'message':msg,'url':url}
                return render(request,'message.html',data)
        else:
            return self.get(request,form)

key = settings.APP_KEY
secret = settings.APP_SECRET
callback = settings.CALLBACK_URL

class SinaLoginView(View):

    def get(self,request):
        client=APIClient(app_key=key,app_secret=secret,redirect_uri=callback)
        url=client.get_authorize_url()
        return redirect(url)

    def post(self,request):
        form=ProfileForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['display_name']
            password='defaultpassword'
            email='defaultemail@qq.com'
            user=User.objects.create_user(username,email,password)
            user.save()
            login(request,user)
            account=user.account
            account.sina_id=form.cleaned_data['sina_id']
            account.display_name=form.cleaned_data['display_name']
            account.homepage=form.cleaned_data['homepage']
            account.biography=form.cleaned_data['biography']
            account.weibo=form.cleaned_data['weibo']
            account.github=form.cleaned_data['github']
            account.save()
            msg='设置成功'
            url=reverse('article:index')
            data={'message':msg,'url':url}
            return render(request,'message.html',data)
        else:
            return self.get(request)

def sina_access(request):
    code=request.GET['code']
    client=APIClient(app_key=key,app_secret=secret,redirect_uri=callback)
    r=client.request_access_token(code)
    sina_id=r.uid
    access_token=r.access_token
    expires_in=r.expires_in
    client.set_access_token(access_token,expires_in)
    try:
        user=Account.objects.get(sina_id=sina_id)
        login(request,user.user)
        msg='登录成功'
        url=reverse('article:index')
        data={'message':msg,'url':url}
        return render(request,'message.html',data)
    except:
        form=ProfileForm(initial={'sina_id':sina_id})
        data={'form':form,'title':'添加信息','is_sina':True,'btn_name':'保存'}
        return render(request,'accounts/settings_profile.html',data)

class LogoutView(View):

    def get(self,request):
        logout(request)
        msg='退出登录'
        url=reverse('article:index')
        data={'message':msg,'url':url}
        return render(request,'message.html',data)

class ProfileView(View):

    @method_decorator(login_required)
    def get(self,request,form=None):
        form_data={
            'display_name':request.user.account.display_name,
            'biography':request.user.account.biography,
            'homepage':request.user.account.homepage,
            'weibo':request.user.account.weibo,
            'github':request.user.account.github
        }
        if not form:
            form=ProfileForm(initial=form_data)
        data={'form':form,'title':'修改资料','is_profile':True,'btn_name':'保存'}
        return render(request,'accounts/settings_profile.html',data)

    @method_decorator(login_required)
    def post(self,request):
        form=ProfileForm(request.POST)
        if form.is_valid():
            account=request.user.account
            account.display_name=form.cleaned_data['display_name']
            account.biography=form.cleaned_data['biography']
            account.homepage=form.cleaned_data['homepage']
            account.weibo=form.cleaned_data['weibo']
            account.github=form.cleaned_data['github']
            account.save()
            msg='成功更新个人资料'
            url=reverse('article:index')
            data={'message':msg,'url':url}
            return render(request,'message.html',data)
        else:
            return self.get(request,form)

class ChangePasswordView(View):

    @method_decorator(login_required)
    def get(self,request,form=None):
        if not form:
            form=ChangePasswordForm(initial={'username':request.user.username})
        data={'form':form,'title':'修改密码','is_password':True,'btn_name':'保存'}
        return render(request,'accounts/settings_profile.html',data)

    @method_decorator(login_required)
    def post(self,request):
        form=ChangePasswordForm(request.POST)
        if form.is_valid():
            password=form.cleaned_data['new_password']
            user=request.user
            user.set_password(password)
            user.save()
            msg='成功修改密码'
            url=reverse('article:login')
            data={'message':msg,'url':url}
            return render(request,'message.html',data)
        else:
            return self.get(request,form)

def test(request):
    return render(request, 'test.html')
