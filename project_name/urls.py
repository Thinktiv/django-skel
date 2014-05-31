from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.http import HttpResponse


from libs.commons import views as commons_views


# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
admin.autodiscover()


if not getattr(settings, 'DEBUG', False):  # only for production
    handler404 = commons_views.Error404.as_view()
    handler500 = commons_views.Error500.as_view()


# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('',
    # Admin panel and documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if not getattr(settings, 'ALLOW_SEARCH_ENGINE_INDEXING', False):
    urlpatterns += patterns('',
        (r'^robots\.txt$', lambda request: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain"))
    )

# Media URL and static URL
if getattr(settings, 'DEVELOPMENT_ENV', False):
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT})
    )
