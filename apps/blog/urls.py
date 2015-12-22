from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^search$', views.search, name='search'),
    url(r'^category/(.*)$', views.view_category, name='category'),
    url(r'^([0-9]+)/([^/]+)$', views.view, name='view'),
    url(r'^([0-9]+)/([^/]+)/view_comments', views.view_comments, name='view_comments'),
    url(r'^([0-9]+)/([^/]+)/comment$', views.comment, name='comment'),
    url(r'^categories.json$', views.categories, name='categories'),
]
