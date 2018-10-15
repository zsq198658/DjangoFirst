# coding:utf-8

from django import forms
from myblogapp.models import UserInfo,User


class GetLoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=20)
    password = forms.CharField(label='密码', max_length=200, widget=forms.PasswordInput)


class GetRegForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=20,)
    password1 = forms.CharField(label='密码', max_length=200, widget=forms.PasswordInput)
    password2 = forms.CharField(label='请再输入一次密码', max_length=200, widget=forms.PasswordInput)


class ChangeInfoForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=20)
    id_number = forms.CharField(label='身份证号', max_length=13)
    sex = forms.ChoiceField(label='性别', widget=forms.RadioSelect, choices=((0, '男'), (1, '女'),))
    age = forms.IntegerField(label='年龄', min_value=0, max_value=200)
    name = forms.CharField(label='姓名', max_length=200)
    image = forms.ImageField(label='头像')
    SEX_CHOICES = (
        (0, u'男'),
        (1, u'女'),
    )
    sex = forms.ChoiceField(choices=SEX_CHOICES)
