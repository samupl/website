from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    date = models.DateTimeField(verbose_name='Date', auto_now_add=True)
    title = models.CharField(verbose_name='Title', max_length=1024)
    slug = models.SlugField(unique=True)
    content = models.TextField(verbose_name='Content')
    comment_count = models.PositiveIntegerField(verbose_name='Comment count', default=0, editable=False)

    @models.permalink
    def get_absolute_url(self):
        return 'blog:view', [str(self.id), str(self.slug)]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{title} ({date})'.format(
            title=self.title,
            date=self.date
        )


class Label(models.Model):
    post = models.ForeignKey(Post)
    label = models.CharField(max_length=90)

    def __str__(self):
        return '{label} ({post})'.format(
            label=self.label,
            post=self.post
        )

    class Meta:
        unique_together = ['post', 'label']


class Comment(models.Model):
    post = models.ForeignKey(Post)
    date = models.DateTimeField(verbose_name='Date', auto_now_add=True)
    username = models.CharField(verbose_name='Username', max_length=256)
    email = models.EmailField(verbose_name='E-mail address')
    content = models.TextField(max_length=4096)
    ip = models.CharField(max_length=4096)
    host = models.CharField(max_length=4096)
    ua = models.CharField(null=True, blank=True, max_length=4096)
    ref = models.CharField(null=True, blank=True, max_length=4096)

    def __str__(self):
        return '{username} ({email}, {ip}, {date}, {post})'.format(
            username=self.username,
            email=self.email,
            ip=self.ip,
            date=self.date,
            post=self.post
        )

@receiver(post_delete, sender=Comment)
@receiver(post_save, sender=Comment)
def calculate_comments_count(sender, instance, **kwargs):
    entry = instance.post
    entry.comment_count = Comment.objects.filter(post=entry).count()
    entry.save()
