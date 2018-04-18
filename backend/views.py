import uuid
import os
import json
from blog import settings
from .forms.form import ArticleForm,BlogForm
from utils.pagination import Pagination

from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse
from .auth.auth import  check_login
from lee import models
from django.db import transaction
from utils.xss import XSSFilter
import datetime as dt

# Create your views here.
@check_login
def index(request):
    return render(request, 'backend_index.html')

@check_login
def base_info(request):
    """
    博主个人信息
    :param request:
    :return:
    """
    nid = request.session['user_info']['nid']
    user = models.UserInfo.objects.filter(nid=nid).first()

    if request.method == 'GET':

        data={
            "username": user.username,
            "email": user.email,
            "nickname": user.nickname,
            "title": '',
            "site": '',
            "theme": '',
        }

        blog = models.Blog.objects.filter(user=nid).first()

        if blog:
            data['title']=blog.title
            data['site'] = blog.site
            data['theme'] = blog.theme

        obj = BlogForm(initial=data)

        return render(request, 'backend_base_info.html', {'obj': obj})

    else: #request.method == 'POST':

        obj = BlogForm(request.POST)

        if obj.is_valid():
            print(obj.cleaned_data)
            nickname = request.POST.get("nickname")

            del obj.cleaned_data['username']
            del obj.cleaned_data['email']
            del obj.cleaned_data['nickname']
            del obj.cleaned_data['site']

            models.Blog.objects.filter(user=nid).update(**obj.cleaned_data)

            models.UserInfo.objects.filter(nid=nid).update(nickname=nickname)

            return redirect('/backend/base-info.html')

        else:
            print(obj.errors)
            return render(request, 'backend_base_info.html', {'obj': obj})

@check_login
def upload_avatar(request):
    ret = {'status': False, 'data': None, 'message': None}
    if request.method == 'POST':
        file_obj = request.FILES.get('avatar_img')
        print(file_obj)
        if not file_obj:
            pass
        else:
            file_name = str(uuid.uuid4())
            file_path = os.path.join('static/imgs/avatar', file_name)
            f = open(file_path, 'wb')
            for chunk in file_obj.chunks():
                f.write(chunk)
            f.close()
            ret['status'] = True
            ret['data'] = file_path

    return HttpResponse(json.dumps(ret))


@check_login
def tag(request):
    """
    博主个人标签管理
    :param request:
    :return:
    """
    #nid = request.session['user_info']['nid']
    blog_id = request.session['user_info']['blog__nid']

    if request.method == 'POST':

        ret = {'status': True, 'error': None, 'data': None}

        o = request.POST.get('o')
        t = request.POST.get('title')

        if o =="add":

            t1= models.Tag.objects.filter(blog = blog_id,title=t).first()

            if t1:
                ret['status'] = False
                ret['error'] = "标签重复"
            else:

                #blog = models.Blog.objects.filter(user=nid).first()
                #nd =blog.nid
                models.Tag.objects.create(title=t,blog_id = blog_id)

        elif o =="del":

            models.Tag.objects.filter(title=t).delete()

        else:
            pass


        return HttpResponse(json.dumps(ret))

    else:#GET
        obj = models.Tag.objects.filter(blog=blog_id)
        t = {}
        i = 0

        for item in obj:
            num = models.Article2Tag.objects.filter(tag=item.nid).count()

            t[i] = {}
            t[i]['num'] = num
            t[i]['title'] = item.title
            i += 1

        return render(request,"backend_tag.html",{'obj':t})

@check_login
def category(request):
    """
    博主个人分类管理
    :param request:
    :return:
    """
    #nid = request.session['user_info']['nid']
    blog_id = request.session['user_info']['blog__nid']

    if request.method == 'POST':
        print("category POST",blog_id)

        ret = {'status': True, 'error': None, 'data': None}

        o = request.POST.get('o')
        t = request.POST.get('title')
        print(o,t)

        if o == "add":
            print("category POST ADD", blog_id)

            t1 = models.Category.objects.filter(blog = blog_id,title=t).first()

            if t1:

                ret['status'] = False
                ret['error'] = "分类重复"
            else:

                models.Category.objects.create(title=t, blog_id=blog_id)

        elif o == "del":
            models.Category.objects.filter(title=t).delete()

        else:
            pass

        return HttpResponse(json.dumps(ret))

    else:  # GET
        obj = models.Category.objects.filter(blog=blog_id)
        t={}
        i=0

        for item in obj:
            num =models.Article.objects.filter(category= item.nid).count()

            t[i]={}
            t[i]['num']=num
            t[i]['title'] = item.title
            i +=1

        return render(request, "backend_category.html", {'obj': t})


@check_login
def article(request, *args, **kwargs):
    """
    博主个人文章管理
    :param request:
    :return:
    """
    blog_id = request.session['user_info']['blog__nid']

    if request.method =="GET":

        condition = {}
        for k, v in kwargs.items():
            if v == '0':
                pass
            else:
                condition[k] = v
        condition['blog_id'] = blog_id
        data_count = models.Article.objects.filter(**condition).count()
        page = Pagination(request.GET.get('p', 1), data_count)
        result = models.Article.objects.filter(**condition).order_by('-nid').only('nid', 'title','blog').select_related('blog')[page.start:page.end]
        page_str = page.page_str(reverse('article', kwargs=kwargs))
        category_list = map(lambda item: {'nid': item[0], 'title': item[1]}, models.Article.category_choices)
        type_list = map(lambda item: {'nid': item[0], 'title': item[1]}, models.Article.type_choices)
        kwargs['p'] = page.current_page
        print(category_list)
        return render(request,
                      'backend_article.html',
                      {'result': result,
                       'page_str': page_str,
                       'category_list': category_list,
                       'type_list': type_list,
                       'arg_dict': kwargs,
                       'data_count': data_count
                       }
                      )
    else:#POST
        print("article POST", blog_id)

        ret = {'status': True, 'error': None, 'data': None}

        o = request.POST.get('o')
        t = request.POST.get('title')
        print(o, t)

        if o == "del":

            with transaction.atomic():
                article_id = models.Article.objects.filter(title=t,blog=blog_id)

                models.Article.objects.filter(title=t,blog=blog_id).delete()
                models.Article2Tag.objects.filter(article=article_id).delete()
                models.ArticleDetail.objects.filter(article=article_id).delete()
                models.Comment.objects.filter(article=article_id).delete()
                models.UpDown.objects.filter(article=article_id).delete()

            #models.Article.objects.filter(title=t).delete()

        else:
            pass

        return HttpResponse(json.dumps(ret))


@check_login
def add_article(request):
    """
    添加文章
    :param request:
    :return:
    """
    if request.method == 'GET':

        form = ArticleForm(request=request)
        return render(request, 'backend_add_article.html', {'form': form})
    elif request.method == 'POST':

        form = ArticleForm(request=request, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                tags = form.cleaned_data.pop('tags')
                content = form.cleaned_data.pop('content')
                print(content)
                content = XSSFilter().process(content)
                print('dddd')
                print(content)
                form.cleaned_data['blog_id'] = request.session['user_info']['blog__nid']
                obj = models.Article.objects.create(**form.cleaned_data)
                models.ArticleDetail.objects.create(content=content, article=obj)
                tag_list = []
                for tag_id in tags:
                    tag_id = int(tag_id)
                    tag_list.append(models.Article2Tag(article_id=obj.nid, tag_id=tag_id))
                models.Article2Tag.objects.bulk_create(tag_list)

            return redirect('/backend/article-0-0.html')
        else:
            print('!!!!!!!!',form.errors)
            return render(request, 'backend_add_article.html', {'form': form})
    else:
        print('article error')
        return redirect('/')


@check_login
def edit_article(request, nid):
    """
    编辑文章
    :param request:
    :return:
    """
    blog_id = request.session['user_info']['blog__nid']
    if request.method == 'GET':
        obj = models.Article.objects.filter(nid=nid, blog_id=blog_id).first()
        if not obj:
            return render(request, 'backend_no_article.html')
        tags = obj.tags.values_list('nid')
        if tags:
            tags = list(zip(*tags))[0]
        init_dict = {
            'nid': obj.nid,
            'title': obj.title,
            'summary': obj.summary,
            'category_id': obj.category_id,
            'article_type_id': obj.article_type_id,
            'content': obj.articledetail.content,
            'tags': tags
        }

        form = ArticleForm(request=request, data=init_dict)
        return render(request, 'backend_edit_article.html', {'form': form, 'nid': nid})
    elif request.method == 'POST':
        form = ArticleForm(request=request, data=request.POST)
        if form.is_valid():
            obj = models.Article.objects.filter(nid=nid, blog_id=blog_id).first()
            if not obj:
                return render(request, 'backend_no_article.html')
            with transaction.atomic():
                content = form.cleaned_data.pop('content')
                content = XSSFilter().process(content)
                tags = form.cleaned_data.pop('tags')
                models.Article.objects.filter(nid=obj.nid).update(**form.cleaned_data)
                models.ArticleDetail.objects.filter(article=obj).update(content=content)
                models.Article2Tag.objects.filter(article=obj).delete()
                tag_list = []
                for tag_id in tags:
                    tag_id = int(tag_id)
                    tag_list.append(models.Article2Tag(article_id=obj.nid, tag_id=tag_id))
                models.Article2Tag.objects.bulk_create(tag_list)
            return redirect('/backend/article-0-0.html')
        else:
            return render(request, 'backend_edit_article.html', {'form': form, 'nid': nid})


def upload_image(request,dir_name):

    result = {"error": 1, "message": "上传出错"}
    files = request.FILES.get("imgFile", None)

    if files:

        result = image_upload(files, dir_name)

    print(result)
    dic = {
        'error': 0,
        'url': '/static/2018/2/20130809170025.png',
        'message': '错误了...'
    }
    return HttpResponse(json.dumps(result))

#目录创建
def upload_generation_dir(dir_name):
    today = dt.datetime.today()
    dir_name = dir_name + '%d/%d/' %(today.year,today.month)

    #if not os.path.exists(settings.STATICFILES_DIRS[0] + dir_name):
    #    os.makedirs(settings.STATICFILES_DIRS[0] + dir_name)
    return dir_name

# 图片上传
def image_upload(files, dir_name):
    #允许上传文件类型
    print(dir_name)
    allow_suffix =['jpg', 'png', 'jpeg', 'gif', 'bmp']
    file_suffix = files.name.split(".")[-1]
    if file_suffix not in allow_suffix:
        return {"error": 1, "message": "图片格式不正确"}
    relative_path_file = upload_generation_dir(dir_name)
    print(relative_path_file)
    path=os.path.join(settings.STATICFILES_DIRS[0], relative_path_file)
    print('@@@',path)
    if not os.path.exists(path): #如果目录不存在创建目录
        os.makedirs(path)
    file_name=str(uuid.uuid1())+"."+file_suffix
    path_file=os.path.join(path, file_name)
    file_url = settings.STATIC_URL + relative_path_file + file_name
    open(path_file, 'wb').write(files.file.read()) # 保存图片
    return {"error": 0, "url": file_url,"message": ""}