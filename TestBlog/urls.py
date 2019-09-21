
from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'app'
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('article/<path:slug>/delete/', views.access_limitation_article, name = 'delete'),
    path('article/update/<path:slug>/', views.access_limitation_article, name = 'update'), 
    path('tag/<path:slug>/delete/', views.access_limitation_tag, name = 'tag_delete'),
    path('', include('Main.urls'))
]
