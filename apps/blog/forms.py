from captcha.fields import ReCaptchaField
from django import forms
from apps.blog.models import Comment


class CommentForm(forms.ModelForm):

    captcha = ReCaptchaField()

    class Meta:
        model = Comment
        fields = ['username', 'email', 'content']
