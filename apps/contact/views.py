# -*- coding: utf-8 -*-

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.template.loader import render_to_string

from apps.contact.forms import ContactForm


def send_mail_from_form(form, request):
    data = form.cleaned_data
    message = render_to_string('mail/message.txt', context={
        'message': data.get('message'),
        'request': request,
    })

    email = EmailMessage(
        subject=settings.CONTACT_FORM_SUBJECT_FMT.format(subject=data.get('subject')),
        body=message,
        from_email=settings.CONTACT_FORM_FROM_EMAIL,
        to=[settings.CONTACT_FORM_RCPT],
        reply_to=['{name} <{email}>'.format(name=data.get('name'), email=data.get('email'))]
    )
    email.send()


def contact(request):
    status = 200
    if request.method == "POST":
        form = ContactForm(request.POST)
        if not form.is_valid():
            status = 500
        else:
            send_mail_from_form(form, request)
    else:
        form = ContactForm()

    data = form.errors
    data['__captcha_key'] = CaptchaStore.generate_key()
    data['__captcha_image_src'] = captcha_image_url(data['__captcha_key'])
    response = JsonResponse(data, status=status)
    return response
