# coding:utf-8
from django.shortcuts import render, render_to_response
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt
from myblogapp.models import User, Article, UserInfo, ArtCategory, LikeCount, LikeRecord
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
# 引入创建的表单类
from .form import GetLoginForm, GetRegForm, UserInfoForm


# 把字典递归转化为类
def dict2obj(args):
    class obj(object):
        def __init__(self, d):
            for a, b in d.items():
                if isinstance(b, (list, tuple)):
                    setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
                else:
                    setattr(self, a, obj(b) if isinstance(b, dict) else b)

    return obj(args)


# 月份格式化
def month(mon):
    mon = int(mon)
    mon_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return mon_list[mon - 1]


# 最近更新
def news(Articles):
    new_list = Articles.objects.all().order_by('-create_time')
    if len(new_list) > 5:
        new_list = new_list[0:4]
    return new_list


# 分类列表
def arts(ArtCategorys):
    art_list = ArtCategorys.objects.all()
    return art_list


# 文章展示
def file_list(lists):
        data_list = []
        for each_blog in lists:
            date = each_blog.get_update_time()
            blog_year = date[0:4]
            blog_mon = month(date[5:7])
            blog_day = date[8:10]
            user = User.objects.filter(username__exact=each_blog.author)
            user_info = UserInfo.objects.get(username__exact=user)
            image = user_info.image
            data_dict = {'blog_id': each_blog.id,
                         'blog_title': each_blog.title,
                         'blog_body': each_blog.content[0:60],
                         'blog_author': user_info.nickname,
                         'author_image': image,
                         'blog_image': each_blog.image, # 这里需要修改
                         'num_of_com': each_blog.num_of_com,
                         'num_of_like': each_blog.num_of_like,
                         'year': blog_year,
                         'mon': blog_mon,
                         'day': blog_day,
                         'blog_category': each_blog.category}
            data_list.append(dict2obj(data_dict))
        return data_list


# 主页
def index(request):
    # 判断登录
    username = request.session.get("username")
    if username:
        # 最近更新
        new_list = news(Article)

        # 分类列表
        art_list = ArtCategory.objects.all()
        blog_list = Article.objects.all().order_by('-update_time')
        data_list = file_list(blog_list)

        # 分页显示
        paginator = Paginator(data_list, 5)  # 每页5个内容
        try:
            current_num = int(request.GET.get('page', 1))
            data_list = paginator.page(current_num)
        except EmptyPage:
            data_list = paginator.page(1)
        if paginator.num_pages > 11:  # 如果分页的数目大于11
            if current_num - 5 < 1:  # 你输入的值
                pageRange = range(1, 11)  # 按钮数
            elif current_num + 5 > paginator.num_pages:  # 按钮数加5大于分页数
                pageRange = range(current_num - 5, current_num + 1)  # 显示的按钮数

            else:
                pageRange = range(current_num - 5, current_num + 6)
                # range求的是按钮 如果你的按钮数小于分页数 那么就按照正常的分页数目来显示
        else:
            pageRange = paginator.page_range  # 正常分配

        return render(request, 'index.html', locals())
    else:
        # 如果没有session,重定向到路由 /login/, 返回表单
        uf = GetLoginForm(request.POST)
        return HttpResponseRedirect("/login/", {"uf": uf})


# 分类页
def article(request, art_name):
    # 最近更新
    new_list = news(Article)
    # 分类列表
    art_list = arts(ArtCategory)

    # 分类展示
    data_list = []
    art_name = str(art_name)
    art = ArtCategory.objects.get(name__exact=art_name)
    art_num = art.id
    art_blog_list = Article.objects.filter(category__exact=art_num)
    blog_list = art_blog_list.order_by('-update_time')
    data_list = file_list(blog_list)

    # 分页显示
    paginator = Paginator(data_list, 5)  # 每页5个内容
    try:
        current_num = int(request.GET.get('page', 1))
        data_list = paginator.page(current_num)
    except EmptyPage:
        data_list = paginator.page(1)
    if paginator.num_pages > 11:  # 如果分页的数目大于11
        if current_num - 5 < 1:  # 你输入的值
            pageRange = range(1, 11)  # 按钮数
        elif current_num + 5 > paginator.num_pages:  # 按钮数加5大于分页数
            pageRange = range(current_num - 5, current_num + 1)  # 显示的按钮数

        else:
            pageRange = range(current_num - 5, current_num + 6)
            # range求的是按钮 如果你的按钮数小于分页数 那么就按照正常的分页数目来显示
    else:
        pageRange = paginator.page_range  # 正常分配

    return render_to_response('article.html', locals())


# 写文章页
def blog(request, blog_id):
    the_blog = Article.objects.get(id=blog_id)
    return render_to_response('blog.html', {'blog': the_blog})


# 读文章页
def blog_detailed(request, blog_id):
    # 最近更新
    new_list = news(Article)
    # 分类列表
    art_list = arts(ArtCategory)

    the_Article = Article.objects.get(id=blog_id)
    return render_to_response('blog_detailed.html', locals())


# 更改个人信息页
def change_info(request):
    username = request.session.get('username', 'anybody')  # get返回第一个，filter返回找到的全部
    the_user = User.objects.get(username__exact=username)
    the_userinfo = UserInfo.objects.get(username__exact=username)
    if request.method == 'POST':
        form = change_info(request.POST)
        if form.is_valid():
           pass
    else:
        form = UserInfoForm(request.POST)
        return render_to_response('change_info.html', {'user': the_user, 'userinfo': the_userinfo, 'form': form})


# 错误页
def page_not_found(request):
    return render(request, 'myblog/500.html')


# 注册页
def reg(request):
    # 最近更新
    new_list = news(Article)
    # 分类列表
    art_list = arts(ArtCategory)

    if request.method == 'POST':  # 当提交表单时
        form = GetRegForm(request.POST)  # form 包含提交的数据
        if form.is_valid():  # 如果提交的数据合法
            name = form.cleaned_data['username']
            user = User.objects.filter(username__exact=name)
            if user:
                return HttpResponse('用户名已存在')
            else:
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                create_time = time.localtime()
                if password1 == password2:
                    user1 = User.objects.create(username=name, password=password1)
                    user1.save()
                    request.session['username'] = name
                    return HttpResponseRedirect('/user_index/')
                else:
                    return HttpResponse('两次密码输入不一致')
        else:
            return HttpResponse('输入有误')
    else:  # 当正常访问时
        form = GetRegForm()
        return render(request, 'reg.html', {'form': form, "new_list": new_list, "art_list": art_list})


# 登录页
# @csrf_exempt
def login(request):
    # 最近更新
    new_list = news(Article)
    # 分类列表
    art_list = arts(ArtCategory)

    if request.method == "POST":
        uf = GetLoginForm(request.POST)
        if uf.is_valid():
            uf_username = uf.cleaned_data["username"]
            uf_password = uf.cleaned_data["password"]
            user = User.objects.filter(username=uf_username, password=uf_password)
            if user:
                request.session["username"] = user[0].username
                # 校验通过,重定向到主页
                return HttpResponseRedirect("/index/")
            else:
                # 检验未通过
                return HttpResponse('用户名密码错误')
        else:
            # 输入错误
            return HttpResponse('输入有误')
    else:
        uf = GetLoginForm()
        return render(request, "login.html", {"form": uf, "new_list": new_list, "art_list": art_list})


# 注销
def logout(request):
    del request.session["username"]  # 删除session
    uf = GetLoginForm(request.POST)
    return HttpResponseRedirect("/login/", {"uf": uf})


# 个人主页
def user_index(request):
    # 最近更新
    new_list = news(Article)
    # 分类列表
    art_list = arts(ArtCategory)

    username = request.session.get('username', 'anybody')
    # username = request.COOKIES.get('username','')           cookie做法，获得COOKIE
    # create_times = User.objects.filter(username__exact=username).values('create_time')
    # print(create_times)
    blog_list = Article.objects.filter(author_id__exact=username)

    if blog_list:
        # 分页显示
        paginator = Paginator(blog_list, 30)  # 每页5个内容
        try:
            current_num = int(request.GET.get('page', 1))
            blog_list = paginator.page(current_num)
        except EmptyPage:
            blog_list = paginator.page(1)
        if paginator.num_pages > 11:  # 如果分页的数目大于11
            if current_num - 5 < 1:  # 你输入的值
                pageRange = range(1, 11)  # 按钮数
            elif current_num + 5 > paginator.num_pages:  # 按钮数加5大于分页数
                pageRange = range(current_num - 5, current_num + 1)  # 显示的按钮数

            else:
                pageRange = range(current_num - 5, current_num + 6)
                # range求的是按钮 如果你的按钮数小于分页数 那么就按照正常的分页数目来显示
        else:
            pageRange = paginator.page_range  # 正常分配
        return render_to_response('user_index.html', locals())
    else:
        return render_to_response('user_index.html', {'username': username})

# 关注与被关注----------------------------------------------------------------------------------------------------


# 点赞操作--------------------------------------------------------------------------------------------------------
# 数据操作成功返回数据方法
def success_response(like_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['like_num'] = like_num
    return JsonResponse(data)


# 数据操作失败返回信息的方法
def error_response(message):
    data = {}
    data['status'] = 'ERROR'
    data['message'] = message
    return JsonResponse(data)


def like_up(request):
    # 得到GET中的数据以及当前用户
    user = request.session.get("username")
    # 判断用户是否登录
    if not user.is_authenticated:
        return error_response('未登录，不能进行点赞操作')
    content_type = request.GET.get('content_type')
    content_type = ContentType.objects.get(model=content_type)
    object_id = request.GET.get('object_id')
    is_like = request.GET.get('is_like')

    # 创建一个点赞记录
    if is_like == 'true':
        # 进行点赞，即实例化一个点赞记录
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id,
                                                                like_user=user)
        # 通过created来判断点赞记录是否存在，如果存在则不进行点赞，如果不存在则进行点赞数量加一
        if created:
            # 不存在点赞记录并且已经创建点赞记录，需要将点赞数量加一
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.like_num += 1
            like_count.save()
            return success_response(like_count.like_num)
        else:
            # 已经进行过点赞
            return error_response('已经点赞过')
    else:
        # 取消点赞
        # 先查询数据是否存在，存在则进行取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, like_user=user).exists():
            # 数据存在，取消点赞
            # 删除点赞记录
            LikeRecord.objects.get(content_type=content_type, object_id=object_id, like_user=user).delete()
            # 判断对应的点赞数量数据是否存在，如果存在则对点赞数量进行减一
            like_count, create = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if create:
                # 数据不存在，返回错误信息
                return error_response('数据不存在，不能取消点赞')
            else:
                # 数据存在，对数量进行减一
                like_count.like_num -= 1
                like_count.save()
                return success_response(like_count.like_num)
        else:
            # 数据不存在，不能取消点赞
            return error_response('数据不存在，不能取消点赞')

# 评论操作--------------------------------------------------------------------------------------------------------