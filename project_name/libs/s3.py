from django.conf import settings
from storages.backends.s3boto import S3BotoStorage


class HerokuStaticS3BotoStorage(S3BotoStorage):
    def __init__(self, *args, **kwargs):
        kwargs['bucket'] = getattr(settings, 'AWS_STATIC_STORAGE_BUCKET_NAME', None)
        kwargs['acl'] = getattr(settings, 'AWS_STATIC_DEFAULT_ACL', 'public-read')
        kwargs['querystring_auth'] = getattr(settings, 'AWS_STATIC_QUERYSTRING_AUTH', False)
        kwargs['preload_metadata'] = getattr(settings, 'AWS_STATIC_PRELOAD_METADATA', True)
        super(HerokuStaticS3BotoStorage, self).__init__(*args, **kwargs)

    #Workaround for bug - http://code.larlet.fr/django-storages/issue/121/s3boto-admin-prefix-issue-with-django-14
    def url(self, name):
        url = super(HerokuStaticS3BotoStorage, self).url(name)
        if name.endswith('/') and not url.endswith('/'):
            url += '/'
        return url
