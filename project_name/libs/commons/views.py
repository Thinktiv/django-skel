from django.views import generic as generic_views

from libs.commons import (
    mixins as commons_mixins,
    utils as commons_utils
)


class Error404(generic_views.TemplateView):
    template_name = '404.html'
    status_code = 404

    def dispatch(self, request, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs), status=self.status_code).render()


class Error500(Error404):
    template_name = '500.html'
    status_code = 500


class AjaxView(commons_mixins.AjaxRequiredMixin, generic_views.View):
    response_class = commons_utils.JSONResponse


class AjaxTemplateView(commons_mixins.AjaxRequiredMixin, generic_views.TemplateView):
    response_class = commons_utils.JSONTemplateResponse
