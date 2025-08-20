from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, Post
 


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        else:
            user = User.objects.create_user(username=username, password=password)
            Profile.objects.create(user=user)  
            login(request, user)
            return redirect('user_profile', username=username)
    return render(request, 'registration/signup.html')



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('feed')  
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=profile_user)
    posts = Post.objects.all()

    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = profile.followers.filter(id=request.user.id).exists()

    return render(request, 'profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'posts': posts,
        'is_following': is_following,
    })



@login_required
def follow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    target_profile = Profile.objects.get(user=target_user)
    target_profile.followers.add(request.user)
    return redirect('user_profile', username=username)


@login_required
def unfollow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    target_profile = Profile.objects.get(user=target_user)
    target_profile.followers.remove(request.user)
    return redirect('user_profile', username=username)

  


