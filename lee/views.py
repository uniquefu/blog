from django.shortcuts import render
import uuid
import os
import json
from blog import settings

from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse
from lee import models
from django.db import transaction
from utils.xss import XSSFilter
import datetime as dt

# Create your views here.
def kind(request):
    return render(request, 'kind.html')

def upload_image(request):

    '''result = {"error": 1, "message": "上传出错"}
    files = request.FILES.get("imgFile", None)

    if files:

        result = image_upload(files, dir_name)

    result['url']='/static/imgs/o_Warning.png'''
    dic = {
        'error': 0,
        'url': '/static/imgs/avatar/20130809170025.png',
        'message': '错误了...'
    }
    return HttpResponse(json.dumps(dic))

#目录创建
def upload_generation_dir(dir_name):
    today = dt.datetime.today()
    dir_name = dir_name + '/%d/%d/' %(today.year,today.month)

    if not os.path.exists(settings.MEDIA_ROOT + dir_name):
        os.makedirs(settings.MEDIA_ROOT + dir_name)
    return dir_name

# 图片上传
def image_upload(files, dir_name):
    #允许上传文件类型
    allow_suffix =['jpg', 'png', 'jpeg', 'gif', 'bmp']
    file_suffix = files.name.split(".")[-1]
    if file_suffix not in allow_suffix:
        return {"error": 1, "message": "图片格式不正确"}
    relative_path_file = upload_generation_dir(dir_name)
    print(relative_path_file)
    path=os.path.join(settings.MEDIA_ROOT, relative_path_file)
    print('@@@',path)
    if not os.path.exists(path): #如果目录不存在创建目录
        os.makedirs(path)
    file_name=str(uuid.uuid1())+"."+file_suffix
    path_file=os.path.join(path, file_name)
    file_url = settings.MEDIA_URL + relative_path_file + file_name
    open(path_file, 'wb').write(files.file.read()) # 保存图片
    return {"error": 0, "url": file_url,"message": ""}
