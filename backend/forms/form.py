#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.core.exceptions import ValidationError
from django import forms as django_forms
from django.forms import fields as django_fields
from django.forms import widgets as django_widgets

from lee import models

class TagForm(django_forms.Form):
    title = django_fields.CharField(
        max_length=32,
        error_messages={'required': '用户名不能为空',
                        'max_length': '用户名最不超过为32个字符'},
        widget=django_widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入标签名'})
    )

class ArticleForm(django_forms.Form):
    title = django_fields.CharField(
        max_length=128,
        error_messages={'required': '标题不能为空',
                        'max_length': '标题最不超过为128个字符'},
        widget=django_widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '文章标题'})

    )
    summary = django_fields.CharField(
        required=False,
        max_length=255,
        error_messages={
                        'max_length': '文章简介最不超过为255个字符'},
        widget=django_widgets.Textarea(attrs={'class': 'form-control', 'placeholder': '文章简介', 'rows': '3'})
    )
    content = django_fields.CharField(
        error_messages={'required': '标题不能为空',},
        widget=django_widgets.Textarea(attrs={'class': 'kind-content','name':"content"})
    )
    article_type_id = django_fields.IntegerField(
        error_messages={'required': '请选择文章类型', },
        widget=django_widgets.RadioSelect(choices=models.Article.type_choices)
    )
    category_id = django_fields.IntegerField(
        error_messages={'required': '请选择分类类型', },
        widget=django_widgets.RadioSelect(choices=models.Article.category_choices)
    )

    tags = django_fields.MultipleChoiceField(
        choices=[],
        widget=django_widgets.CheckboxSelectMultiple
    )

    def __init__(self, request, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        blog_id = request.session['user_info']['blog__nid']
        #self.fields['category_id'].choices = models.Article.objects.filter(blog_id=blog_id).values_list('nid','title')
        self.fields['tags'].choices = models.Tag.objects.filter(blog_id=blog_id).values_list('nid', 'title')
		
		
class BlogForm(django_forms.Form):
    theme =django_fields.ChoiceField(
        required=False,
        choices=[(0,"默认主题"),(1,"体育"),(2,"财经"),(3,"娱乐")]
    )

    site = django_fields.CharField(
        required=False,
		disabled=True,
        widget=django_widgets.TextInput(attrs={'class': "form-control",
              'placeholder': '如：wupeiqi,则个人博客为http://www.xxx.com/wupeiqi.html'})
        )
        
    title = django_fields.CharField(
        required=False,
        widget=django_widgets.Textarea(attrs={'class': 'form-control',
            'style':'min-height: 100px','placeholder': '来一杯鸡汤...'})
    )

    username = django_fields.CharField(
        required=False,
        disabled=True,
        widget=django_widgets.TextInput(attrs={'class': 'form-control'})

    )

    email = django_fields.CharField(
        required=False,
        disabled= True,
        widget=django_widgets.TextInput(attrs={'class': 'form-control'})

    )

    nickname = django_fields.CharField(
        required=False,
        widget=django_widgets.TextInput(attrs={'class': 'form-control'})
    )

