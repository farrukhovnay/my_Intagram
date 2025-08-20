from django.urls import path
from . import views
from .views import login_view
urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('<str:username>/', views.profile_view, name='user_profile'),
    path('<str:username>/follow/', views.follow_user, name='follow_user'),
    path('<str:username>/unfollow/', views.unfollow_user, name='unfollow_user'),
    
]

