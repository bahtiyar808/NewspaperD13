import datetime

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


from newspaper import settings
from newsapp.models import Post

from newsapp.models import Category


@shared_task
def send_notifications(preview, pk, title):
    instance = Post.objects.get(id=pk)
    categories = instance.categories.all()
    subscribers = []
    for category in categories:
        subscribers += category.subscribers.all()

    subscribers = [s.email for s in subscribers]
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'http://127.0.0.1:8000/newspaper/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@shared_task
def notif_every_week():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(date_time__gte=last_week)
    categories = set(posts.values_list('categories__category_name', flat=True))
    subscribers = set(Category.objects.filter(category_name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': 'http://127.0.0.1:8000',
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject= 'Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

