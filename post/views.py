from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Post
from .forms import PostForm, CommentForm
from django.db.models import Q, Max
from .models import Message
from .forms import MessageForm
from .models import Post, Story
from .forms import StoryForm

def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    stories = Story.objects.all().order_by('-created_at')
    context = {
        'posts': posts,
        'stories': [s for s in stories if s.is_active()]
    }
    return render(request, 'feed.html', context)

@login_required
def add_story(request):
    if request.method == "POST":
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            return redirect('feed') 
    return redirect('feed')


@login_required
def view_story(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    if not story.is_active():
        return redirect('feed')
    return render(request, 'story_view.html', {'story': story})



@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at') 
    
    if request.method == 'POST':
        c_form = CommentForm(request.POST)
        if c_form.is_valid():
            comment = c_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('detail', post_id=post.id)
    else:
        c_form = CommentForm()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,   
        'c_form': c_form
    })

from .models import Like

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like_obj = Like.objects.filter(post=post, user=request.user).first()

    if like_obj:
        like_obj.delete()  
    else:
        Like.objects.create(post=post, user=request.user)  
    return redirect('feed')



User = get_user_model()

@login_required
def dm_inbox(request):
    """Show inbox with all users, highlight recent chat partners with last message."""
    
    
    threads = (
        Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
        .values('sender', 'recipient')
        .annotate(last_time=Max('created_at'))
        .order_by('-last_time')
    )

    partners_ids = set()
    for t in threads:
        other_id = t['recipient'] if t['sender'] == request.user.id else t['sender']
        partners_ids.add(other_id)
    partners = User.objects.filter(id__in=partners_ids)

    
    last_by_partner = {}
    for p in partners:
        last_msg = (
            Message.objects.filter(
                Q(sender=request.user, recipient=p) |
                Q(sender=p, recipient=request.user)
            )
            .order_by('-created_at')
            .first()
        )
        last_by_partner[p.username] = last_msg

    
    all_users = User.objects.exclude(id=request.user.id)

    context = {
        'partners': partners,                
        'last_by_partner': last_by_partner,  
        'all_users': all_users,              
    }
    return render(request, 'inbox.html', context)


@login_required
def dm_start(request, username):
    """Start a thread with a user (redirects to thread, optionally pre-fills form)."""
    other = get_object_or_404(User, username=username)
    if other == request.user:
        return redirect('dm_inbox')
    return redirect('dm_thread', username=other.username)

@login_required
def dm_thread(request, username):
    """Show a 1:1 thread and a form to send a message."""
    other = get_object_or_404(User, username=username)
    if other == request.user:
        return redirect('dm_inbox')

    qs = Message.objects.filter(
        Q(sender=request.user, recipient=other) |
        Q(sender=other, recipient=request.user)
    ).order_by('created_at')

    
    qs.filter(recipient=request.user, is_read=False).update(is_read=True)

    form = MessageForm()
    return render(request, 'thread.html', {
        'other': other,
        'messages_qs': qs,
        'form': form,
    })

@login_required
def dm_send(request, username):
    """Handle POST from the thread form."""
    other = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            Message.objects.create(
                sender=request.user,
                recipient=other,
                body=form.cleaned_data['body']
            )
    return redirect('dm_thread', username=other.username)


