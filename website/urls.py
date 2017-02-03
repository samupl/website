from django.conf.urls import include, url
from django.contrib import admin
import apps.pages.urls
import apps.contact.urls
import apps.blog.urls


urlpatterns = [
    url(r'^', include(apps.pages.urls, namespace='pages')),
    url(r'^blog/', include(apps.blog.urls, namespace='blog')),
    url(r'^contact', include(apps.contact.urls, namespace='contact')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^\.well-known/keybase\.txt', 'apps.keybase.views.proof'),
]
