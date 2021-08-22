from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from pin.models import Profile


def send_activation_code(email, activation_code, status):
    if status == 'register':
        context = {
            'domain': 'http://localhost:8000',
            'activation_code': activation_code
        }
        msg_html = render_to_string('activate.html', context)
        message = strip_tags(msg_html)
        send_mail(
            'Activate your account',
            message,
            'pinterest@gmail.com',
            [email],
            html_message=msg_html,
            fail_silently=False
        )
    elif status == 'reset_password':
        context = {
            'activation_code': activation_code
        }
        msg_html = render_to_string('reset.html', context)
        message = strip_tags(msg_html)
        send_mail(
            'Reset your password',
            message,
            'pinterest@gmail.com',
            [email],
            html_message=msg_html,
            fail_silently=False
        )


def send_notification(followed_to, user, post):
    context = {
        'link': f'http://localhost:8000/api/pins/{post.id}/',
        'username': followed_to.username,
        'pin_title': post.title[:15] + '...'
    }
    msg_html = render_to_string('notification.html', context)
    message = strip_tags(msg_html)
    send_mail(
        f'{followed_to.username} posted a new pin!',
        message,
        'pinterest@gmail.com',
        [user.email],
        html_message=msg_html,
        fail_silently=False
    )


def create_profile(user):
    return Profile.objects.create(author=user)
