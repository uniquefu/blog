from io import BytesIO
import json

from django.shortcuts import render, HttpResponse,redirect

from lee import models
from utils.check_code import create_validate_code
from web.forms.form import RegisterForm,LoginForm

from lee import models


# Create your views here.
'''def index(request):
    """
        博客首页，展示全部博文
        :param request:
        :return:
        """

    article_type_list = models.Article.type_choices
    return  render(request, 'index.html', {'article_type_list': article_type_list, })'''

def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())

def logout(request):
    request.session.clear()

    return redirect('/')

	
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == 'POST':

        result = {'status': False, 'message': None, 'data': None}
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user_info = models.UserInfo.objects. \
                filter(username=username, password=password). \
                values('nid', 'nickname',
                       'username', 'email',
                       'blog__nid',
                       'blog__site').first()

            if not user_info:
                result['message'] = '用户名或密码错误'
            else:
                result['status'] = True
                request.session['user_info'] = user_info
				
                if form.cleaned_data.get('rmb'):
                    request.session.set_expiry(60 * 60 * 24 * 31)
        else:
            print(form.errors)
            if 'check_code' in form.errors:
                result['message'] = '验证码错误或者过期'
            else:
                result['message'] = '用户名或密码错误'
        return HttpResponse(json.dumps(result))
	
def register(request):
    if request.method=="GET":
        obj = RegisterForm(request=request)
        return render(request, 'register.html', {'obj': obj})
		
    else:#POST

        obj = RegisterForm(request=request,data=request.POST)

        if obj.is_valid():

            del obj.cleaned_data['check_code']
            del obj.cleaned_data['repassword']

            print(obj.cleaned_data)

            site = request.POST.get('username')


            u=models.UserInfo.objects.create(**obj.cleaned_data)

            models.Blog.objects.create(user=u,site=site)

            return redirect('/')
        else:
            print(obj.errors)
            return render(request, 'register.html', {'obj':obj})



