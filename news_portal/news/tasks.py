from celery import shared_task
import datetime
from django.conf import settings
from .models import Post, Category
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def send_email_news(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    title = post.title
    subscribers_emails = []
    for category in categories:
        subscribers_users = category.subscribers.all()
        for sub_user in subscribers_users:
            subscribers_emails.append(sub_user.email)

    html_content = render_to_string(
        'sent_email.html',
        {
            'text': post.preview,
            'link': f'{settings.SITE_URL}/news/{pk}',

        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email='ilhaosinkin@yandex.ru',
        to=subscribers_emails,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)


@shared_task
def weekly_notification():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_in__gte=last_week)
    categories = set(posts.values_list('category__tematic', flat=True))
    subscribers = set(Category.objects.filter(tematic__in=categories).values_list('subscribers', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за Неделю',
        body='',
        from_email='ilhaosinkin@yandex.ru',
        to=subscribers,
    )
    msg.attach_alternative(html_content, "text/html")

    msg.send(fail_silently=False)