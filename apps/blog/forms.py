from captcha.fields import CaptchaField
from django import forms
from django.utils.translation import ugettext_lazy
from apps.blog.models import Comment


class CommentForm(forms.ModelForm):

    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ['username', 'email', 'content']
