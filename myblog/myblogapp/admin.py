# Register your models here.
from django.contrib import admin
from myblogapp.models import User, UserInfo, Article, CommentArt, CommentCom, LikeArt, LikeCom, ArtCategory, Comment, Like

admin.site.register(User)
admin.site.register(UserInfo)
admin.site.register(Article)
admin.site.register(ArtCategory)
admin.site.register(CommentArt)
admin.site.register(CommentCom)
admin.site.register(LikeArt)
admin.site.register(LikeCom)
admin.site.register(Comment)
admin.site.register(Like)

