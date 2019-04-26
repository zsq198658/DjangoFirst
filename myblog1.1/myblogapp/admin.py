# Register your models here.
from django.contrib import admin
from myblogapp.models import User, UserInfo, Article, ArtCategory, Comment, CommentArt, CommentCom, LikeCount, \
    LikeRecord
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
admin.site.register(User)
admin.site.register(UserInfo)
admin.site.register(Article)
admin.site.register(ArtCategory)
admin.site.register(Comment)
admin.site.register(CommentArt)
admin.site.register(CommentCom)
admin.site.register(LikeCount)
admin.site.register(LikeRecord)
