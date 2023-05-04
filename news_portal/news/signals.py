from django.conf import settings
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import PostCategory, Post, Author
from django.utils import timezone
from datetime import datetime

def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'sent_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body=preview,
        from_email='ilhaosinkin@yandex.ru',
        to=['ilaosinkin@gmail.com'],
    )
    msg.attach_alternative(html_content, "text/html")

    msg.send(fail_silently=False)

@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers_emails)

@receiver(pre_save, sender = Author)
def check_for_saves(sender, instance, **kwargs):
    current_author = instance.author.id
    current_time = datetime.now(tz=timezone.utc)
    day = datetime(days=1)
    my_time = current_time - day

    for i in Post.objects.all().filter(author=current_author, published_date=my_time):
        if len(i) > 3:
            raise Exception("Sorry, you can't save more than 1 post per day.")