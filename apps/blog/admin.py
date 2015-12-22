from django.contrib import admin
from apps.blog.models import Post, Comment, Label


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'comment_count']
    search_fields = ['title', 'slug']
    prepopulated_fields = {
        'slug': ['title']
    }

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['author'].initial = request.user
        return form


class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'date', 'username', 'email', 'ip', 'host', 'ua', 'ref']


class LabelAdmin(admin.ModelAdmin):
    list_display = ['post', 'label']


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Label, LabelAdmin)
