from django import forms
from .models import Post, Comment, Message, Story

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Add a comment...'})
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Write a message…',
                'class': 'msg-input'
            })
        }
        labels = {'body': ''}


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['image']        

