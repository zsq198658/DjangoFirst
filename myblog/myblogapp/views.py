
# coding:utf-8
from django.shortcuts import render, render_to_response
from myblogapp.models import User, Article, UserInfo
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
# 引入我们创建的表单类
from .form import GetLoginForm, GetRegForm, ChangeInfoForm


def dict2obj(args):
    # 把字典递归转化为类
    class obj(object):
        def __init__(self, d):
            for a, b in d.items():
                if isinstance(b, (list, tuple)):
                    setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
                else:
                    setattr(self, a, obj(b) if isinstance(b, dict) else b)
    return obj(args)


def month(mon):
    mon = int(mon)
    mon_list = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    return mon_list[mon-1]



def index(request):
    blog_list = Article.objects.all().order_by('-update_time')
    new_list = Article.objects.all().order_by('-create_time')
    new_list = new_list[0:4]
    data_list = []
    for each_blog in blog_list:
        date = each_blog.get_update_time()
        blog_year = date[0:4]
        blog_mon = month(date[5:7])
        blog_day = date[8:10]
        user = User.objects.filter(username__exact=each_blog.author)
        user_info = UserInfo.objects.get(username__exact=user)
        image = user_info.image
        data_dict = {'blog_id': each_blog.id, 'blog_title': each_blog.title, 'blog_body': each_blog.content,
                     'blog_author' : each_blog.author, 'author_image': image, 'blog_image': each_blog.image,
                     'num_of_com' : each_blog.num_of_com, 'num_of_like' : each_blog.num_of_like, 'year' : blog_year,
                     'mon' : blog_mon, 'day' : blog_day, 'blog_category': each_blog.category}
        data_list.append(dict2obj(data_dict))

    paginator = Paginator(data_list, 5)
    page = request.GET.get('page', 1)
    try:
        data_list = paginator.page(page)
    except:
        data_list = paginator.page(1)

    return render(request, 'index.html', locals())


def reg(request):
    if request.method == 'POST':  # 当提交表单时
        form = GetRegForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            print(form.cleaned_data)
            name = form.cleaned_data['username']
            user = User.objects.filter(username__exact=name)
            if user:
                return HttpResponse('用户名已存在')
            else:
                passwd = form.cleaned_data['password1']
                passwd2 = form.cleaned_data['password2']
                create_time = time.localtime()
                if passwd == passwd2:
                    print(create_time)
                    user1 = User.objects.create(username=name, passwd=passwd)
                    user1.save()
                    request.session['username'] = name
                    return HttpResponseRedirect('/user_index/')
                else:
                    return HttpResponse('两次密码输入不一致')
        else:
            return HttpResponse('输入有误')
    else:  # 当正常访问时
        form = GetRegForm()
    return render(request, 'reg.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = GetLoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            password = form.cleaned_data['password']
            users = User.objects.filter(username__exact=name, password__exact=password)
            if users:
                # response = HttpResponseRedirect('/index/')    cookie做法，新建cookie
                # response.set_cookie('username', name, 3600)
                request.session['username'] = name
                return HttpResponseRedirect('/user_index/')
            else:
                return render(request, 'login.html', {'form': form})
    else:
        form = GetLoginForm()
        return render(request, 'login.html', {'form': form})


def logout(request):
    del request.session['username']
    return render(request, 'logout.html')
'''   response = HttpResponse('logout')                      cookie做法，删除cookie
    response.delete_cookie('username')
    if request.session['username']:
'''


def user_index(request):
    username = request.session.get('username', 'anybody')
    # username = request.COOKIES.get('username','')           cookie做法，获得COOKIE
    # create_times = User.objects.filter(username__exact=username).values('create_time')
    # print(create_times)
    blog_list = Article.objects.filter(author__username__exact=username)
    if blog_list:
        return render_to_response('user_index.html', {'username': username, 'blogs': blog_list})
    else:
        return render_to_response('user_index.html', {'username': username})


def blog(request, blog_id):
    the_blog = Article.objects.get(id=blog_id)
    return render_to_response('blog.html', {'blog': the_blog})


def blog_detailed(request, blog_id):
    the_Article = Article.objects.get(id=blog_id)
    return render_to_response('blog_detailed.html', {'Article': the_Article})


def change_info(request):
    username = request.session.get('username', 'anybody')
    the_user = User.objects.filter(username__exact=username)
    the_userinfo = UserInfo.objects.filter(username__exact=username)
    form = ChangeInfoForm(request.POST)
    print(the_user)
    return render_to_response('change_info.html', {'user': the_user})




