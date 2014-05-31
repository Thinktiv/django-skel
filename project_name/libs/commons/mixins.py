from django.http import Http404
from django import forms
import django.forms.forms


class PreDispatchMixin(object):
    """
    Mixin to implement some functionality before making call to dispatch
    """
    def pre_dispatch(self, request, *args, **kwargs):
        raise NotImplementedError()

    def dispatch(self, request, *args, **kwargs):
        self.pre_dispatch(request, *args, **kwargs)
        return super(PreDispatchMixin, self).dispatch(request, *args, **kwargs)


class AjaxRequiredMixin(PreDispatchMixin):
    """
    Mixin which restricts access to only Ajax requests, for a View
    """
    def pre_dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404()


class FormUtilMixin(object):
    """
    Contains general utility functions for forms
    """
    def add_error(self, field, error):
        """
        ```
        This method would be added to django.forms.forms.BaseForm in Django-1.7,
        See: https://github.com/django/django/blob/2692a0c6217b1b5ea2730f5861cb96c991fc8673/django/forms/forms.py
        ```

        Update the content of `self._errors`.

        The `field` argument is the name of the field to which the errors
        should be added. If its value is None the errors will be treated as
        NON_FIELD_ERRORS.

        The `error` argument can be a single error, a list of errors, or a
        dictionary that maps field names to lists of errors. What we define as
        an "error" can be either a simple string or an instance of
        ValidationError with its message attribute set and what we define as
        list or dictionary can be an actual `list` or `dict` or an instance
        of ValidationError with its `error_list` or `error_dict` attribute set.

        If `error` is a dictionary, the `field` argument *must* be None and
        errors will be added to the fields that correspond to the keys of the
        dictionary.
        """
        if not isinstance(error, forms.ValidationError):
            # Normalize to ValidationError and let its constructor
            # do the hard work of making sense of the input.
            error = forms.ValidationError(error)

        if hasattr(error, 'error_dict'):
            if field is not None:
                raise TypeError(
                    "The argument `field` must be `None` when the `error` "
                    "argument contains errors for multiple fields."
                )
            else:
                error = error.error_dict
        else:
            error = {field or django.forms.forms.NON_FIELD_ERRORS: error.messages}

        for field, error_list in error.items():
            if field not in self.errors:
                if field != django.forms.forms.NON_FIELD_ERRORS and field not in self.fields:
                    raise ValueError(
                        "'%s' has no field named '%s'." % (self.__class__.__name__, field))
                self._errors[field] = self.error_class()
            self._errors[field].extend(error_list)
            if field in self.cleaned_data:
                del self.cleaned_data[field]
