from captcha.fields import ReCaptchaField
from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField(label="E-mail address")
    subject = forms.CharField(label="Subject", max_length=255)
    name = forms.CharField(label="Name", max_length=255)
    message = forms.CharField(label="Message",
                              max_length=4096,
                              widget=forms.Textarea)
    captcha = ReCaptchaField()
