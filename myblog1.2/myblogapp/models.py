# coding:utf-8
# Create your models here.

from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import DjangoUeditor
# from django.contrib.auth.hashers import make_password, check_password


# 账号密码类
class User(models.Model):
    username = models.CharField('登录名', max_length=60, primary_key=True, unique=True)
    password = models.CharField('密码', max_length=60)
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('密码最后修改日期', auto_now=True)

    def __str__(self):
        return self.username

    def get_create_time(self):
        return self.create_time.strftime("%Y-%m-%d %H:%M:%S")

    def get_update_time(self):
        return self.update_time.strptime("%Y-%m-%d %H:%M:%S")


#    def save(self):
#        self.password = make_password(self.password)
#       super(User, self).save()


# 用户信息类
class UserInfo(models.Model):
    username = models.OneToOneField('User', db_constraint=False)
    SEX_CHOICES = (
        (0, u'男'),
        (1, u'女'),
    )
    nickname = models.CharField('用户名', max_length=30, primary_key=True, unique=True)
    name = models.CharField('真实姓名', max_length=20, blank=True, null=True)
    b_day = models.DateField('出生日期', blank=True, null=True)
    gender = models.BooleanField('性别', max_length=2, choices=SEX_CHOICES)
    image = models.ImageField('头像', upload_to='static/image/user_logo/%Y/%m/%d',
                              blank=True, default='static/image/image.jpg')
    address = models.CharField('地址', max_length=100, blank=True, null=True)
    phone = models.CharField('电话', max_length=13, blank=True, null=True)
    introduction = DjangoUeditor.models.UEditorField('简介', width=900, height=300,
                                                     toolbars="full", imagePath="", filePath="",
                                                     upload_settings={"imageMaxSize": 1204000},
                                                     settings={}, command=None, blank=True)
    update_time = models.DateTimeField('最后修改日期', auto_now=True)

    def __str__(self):
        return self.nickname

    def get_update_time(self):
        return self.update_time.strptime("%Y-%m-%d %H:%M:%S")


# 用户最近浏览类
class UserRecView(models.Model):
    read_user = models.ForeignKey('User')
    read_article = models.ForeignKey('Article')

    def __str__(self):
        return self.read_user.username


# 文章类
class Article(models.Model):
    title = models.CharField('标题', max_length=200)
    author = models.ForeignKey('User', db_constraint=False)
    num_of_view = models.IntegerField('访问量', default=0)
    num_of_com = models.IntegerField('评论数', default=0)
    num_of_like = models.IntegerField('点赞数', default=0)
    content = DjangoUeditor.models.UEditorField('内容 ', width=900, height=600,
                                                toolbars="full", imagePath="", filePath="",
                                                upload_settings={"imageMaxSize": 1204000},
                                                settings={}, command=None, blank=True)
    category = models.ForeignKey('ArtCategory', db_constraint=False)
    image = models.ImageField('图片', upload_to='static/image/article_image/%Y/%m/%d',
                              blank=True, default='static/image/Art_Image.jpg')
    create_time = models.DateTimeField('创建日期', auto_now_add=True)
    update_time = models.DateTimeField('最后修改日期', auto_now=True)

    def __str__(self):
        return self.title

    def get_content(self):
        return self.content[0:50]

    def get_create_time(self):
        return self.create_time.strftime("%Y-%m-%d %H:%M:%S")

    def get_update_time(self):
        return self.update_time.strftime("%Y-%m-%d %H:%M:%S")


# 文章类别类
class ArtCategory(models.Model):
    name = models.CharField('类别名称', max_length=20, unique=True)

    def __str__(self):
        return self.name


# 评论类
class Comment(models.Model):
    com_user = models.ForeignKey('User', db_constraint=False)
    com_time = models.DateTimeField('评论时间', auto_now=True)
    com_text = models.CharField('评论内容', max_length=200)
    num_of_com = models.IntegerField('评论数', default=0)

    def __str__(self):
        return self.com_text[:20]

    def get_com_time(self):
        return self.com_time.strftime("%Y-%m-%d %H:%M:%S")


# 评论的文章类
class CommentArt(Comment):
    com_obj = models.ForeignKey('Article', db_constraint=False)


# 评论的状态类
class CommentCom(Comment):
    com_obj = models.ForeignKey('CommentArt', db_constraint=False)


# 用于记录点赞数量的模型
class LikeCount(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    # 用于记录点赞数量的字段
    like_num = models.IntegerField(default=0)


# 用于记录点赞状态的模型
class LikeRecord(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    # 记录点赞的用户
    like_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # 记录点赞的时间
    like_time = models.DateTimeField(auto_now_add=True)
