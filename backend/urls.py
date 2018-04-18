"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from  backend import views

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^index.html$',views.index ),
    url(r'^base-info.html$', views.base_info),
    url(r'^tag.html$', views.tag),
    url(r'^category.html$', views.category),
    url(r'^article-(?P<article_type_id>\d+)-(?P<category_id>\d+).html$', views.article, name='article'),
    url(r'^add-article.html$', views.add_article),
    url(r'^edit-article-(?P<nid>\d+).html$', views.edit_article),
    url(r'^upload-avatar.html$', views.upload_avatar),
    url(r'^uploads/(?P<dir_name>)$',views.upload_image),

]
