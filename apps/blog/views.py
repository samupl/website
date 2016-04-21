from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.db.models import Count
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django_gravatar.helpers import get_gravatar_url
from apps.blog.forms import CommentForm
from apps.blog.models import Post, Comment, Label


def home(request):
    entries = Post.objects.all().order_by('-date')
    return render(request, 'blog/index.html', {
        'entries': entries
    })


def view(request, post_id, post_slug):
    try:
        entry = Post.objects.get(pk=post_id, slug=post_slug)
    except Post.DoesNotExist:
        raise Http404

    form = CommentForm

    return render(request, 'blog/view.html', {
        'entry': entry,
        'form': form
    })


def view_comments(request, post_id, post_slug):
    try:
        entry = Post.objects.get(pk=post_id, slug=post_slug)
    except Post.DoesNotExist:
        raise Http404

    comments_qs = Comment.objects.filter(post=entry)
    comments = [
        {
            'date': c.date,
            'username': c.username,
            'avatar': get_gravatar_url(c.email),
            'content': c.content,
        } for c in comments_qs]
    return JsonResponse({
        'comments': comments,
        'count': comments_qs.count(),
    })


def comment(request, post_id, post_slug):
    try:
        entry = Post.objects.get(pk=post_id, slug=post_slug)
    except Post.DoesNotExist:
        raise Http404

    status = 200
    if request.method == "POST":
        form = CommentForm(request.POST)
        if not form.is_valid():
            status = 500
        else:
            data = form.cleaned_data
            Comment.objects.create(
                username=data.get('username'),
                email=data.get('email'),
                content=data.get('content'),
                post=entry,
                ip=request.META['REMOTE_ADDR'],
                ua=request.META['HTTP_USER_AGENT'],
                ref=request.META.get('HTTP_REFERER', None)
            )
    else:
        form = CommentForm()

    data = form.errors
    data['__captcha_key'] = CaptchaStore.generate_key()
    data['__captcha_image_src'] = captcha_image_url(data['__captcha_key'])
    response = JsonResponse(data, status=status)
    return response


def categories(request):
    labels = Label.objects.all().values('label').annotate(count=Count('post_id')).order_by('-count')
    return JsonResponse(data={'label_stats': list(labels)})


def view_category(request, category_name):
    labels = Label.objects.filter(label=category_name)
    if labels.count() == 0:
        raise Http404

    return render(request, 'blog/category.html', {'labels': labels, 'category_name': category_name})


def search(request):
    keyword = request.GET.get('q', None)
    if keyword is None:
        raise Http404

    entries = Post.objects.filter(title__contains=keyword)
    return render(request, 'blog/search.html', {'keyword': keyword, 'entries': entries})

