import imp
import json

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template.context import RequestContext


def get_default_django_settings_module():
    try:
        file_ = imp.find_module('dev_local', ['{{ project_name }}/settings'])[0]
    except ImportError:
        default_django_settings_module = "{{ project_name }}.settings.dev"
    else:
        default_django_settings_module = "{{ project_name }}.settings.dev_local"
        file_.close()
    return default_django_settings_module


class JSONResponse(HttpResponse):
    """JSON response class."""
    def __init__(self, obj='', json_opts=None, content_type="application/json", *args, **kwargs):
        content = json.dumps(obj, **json_opts or {})
        super(JSONResponse, self).__init__(content, content_type, *args, **kwargs)


class JSONTemplateResponse(HttpResponse):
    def __init__(self, request, template, context, content_type=None, *args, **kwargs):
        """
        Renders a JSON template and returns an HTTP response
        :param request: HTTP request
        :param template: Name of JSON template to be rendered (usually have .json extension)
        :param context: Context dictionary
        :param json_opts: Dictionary of keyword arguments to be passed to `json.dumps` function
        :param content_type: Content-type of the response. Default is 'application/json'
        """
        # Note: Don't set `content_type="application/json"` as Django's `TemplateResponseMixin` explicitly sets `content_type` to `None` when it's not provided.

        super(JSONTemplateResponse, self).__init__(
            render_to_string(template, context, RequestContext(request)), content_type or "application/json", *args, **kwargs
        )
