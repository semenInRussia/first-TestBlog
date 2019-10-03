
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('article/create/', views.post_create, name = 'createpost'),
    path('article/<path:slug>/delete/', views.delete, name = 'delete'),
    path('article/<path:slug>/tagcreate/', views.createcomment.as_view(), name='createcomment'),
    path('article/update/<path:slug>/', views.update.as_view(), name = 'update'),
    path('articles/<path:slug>', views.detail, name='detail'),
    path('articles/', views.articles , name='articles' ),
    path('articles/<path:slug>', views.createcomment.as_view(), name="detail"),
    path('', views.index , name='index' ),
    path('contacts/', views.contacts , name='contacts' ),

    path('tags/', views.tag_index, name='tags'),
    path('tag/create', views.tag_create.as_view(), name='createtag'),
    path('tag/<path:slug>/update/', views.tag_update.as_view(), name = 'tag_update'),
    path('tag/<path:slug>/delete/', views.tag_delete, name = 'tag_delete'),
    path('tags/<path:slug>', views.tag_detail, name='tag_detail'),

    path('kabinet/<path:username>/logaut/', views.lagaut, name='lagaut'),
    path('registration/', views.registruser.as_view(), name='registr'),
    path('login/', views.userlogin.as_view(), name='login'),
    path('kabinet/<path:username>/', views.kabinet, name='kabinet'),

    path('searctag/', views.searchtag, name='searchtag'),
    path('searcharticle/', views.articleget, name='searcharticle'),
]
