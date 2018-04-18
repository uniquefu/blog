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
from .views import account,home



urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    #url(r'^article-(?P<article_type_id>\d+)-(?P<category_id>\d+).html',views.article ),
    url(r'^$',home.index ),
	url(r'^check_code.html$', account.check_code),
	url(r'^login.html$',account.login ),
	url(r'^logout.html$',account.logout ),
	url(r'^register.html$',account.register ),
	url(r'^all/(?P<article_type_id>\d+).html$', home.index, name='index'),
    url(r'^(?P<site>\w+).html$', home.home),
    url(r'^(?P<site>\w+)/(?P<condition>((tag)|(date)|(category)))/(?P<val>\w+-*\w*).html$', home.filter),
    url(r'^(?P<site>\w+)/(?P<nid>\d+).html$', home.detail),
]