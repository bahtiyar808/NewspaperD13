from allauth.account.forms import SignupForm
from django import forms
from django.core.mail import send_mail, EmailMultiAlternatives

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['heading', 'text', 'post_rate', 'author', 'categories']

