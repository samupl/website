from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from apps.blog.models import Comment


