from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import PostCategory
from django.conf import settings

from .tasks import send_notifications


#
#
# def send_notifications(preview, pk, title, subscribers):
#     html_content = render_to_string(
#         'post_created_email.html',
#         {
#             'text': preview,
#             'link': f'http://127.0.0.1:8000/newspaper/{pk}'
#         }
#     )
#     msg = EmailMultiAlternatives(
#         subject= title,
#         body = '',
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to = subscribers
#     )
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()
#
#
@receiver(m2m_changed, sender=PostCategory)
def new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        send_notifications(instance.preview(), instance.pk, instance.heading)
