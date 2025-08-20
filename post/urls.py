from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('posts/<int:post_id>/', views.post_detail, name='detail'),
    path('messages/', views.dm_inbox, name='dm_inbox'),
    path('messages/start/<str:username>/', views.dm_start, name='dm_start'),
    path('messages/<str:username>/', views.dm_thread, name='dm_thread'),
    path('messages/<str:username>/send/', views.dm_send, name='dm_send'),
    path('add_story/', views.add_story, name='add_story'),
    path('story/<int:story_id>/', views.view_story, name='view_story'),

]
