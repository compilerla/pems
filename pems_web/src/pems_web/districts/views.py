from django.views.generic import TemplateView, DetailView

from .models import District


class DistrictContextMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        districts_ctx = {}
        districts_ctx["all"] = District.objects.all()
        context["districts"] = districts_ctx
        return context


class IndexView(DistrictContextMixin, TemplateView):
    template_name = "districts/index.html"


class DistrictView(DistrictContextMixin, DetailView):
    model = District
    context_object_name = "current_district"
    template_name = "districts/district.html"

    def get_object(self):
        return District.objects.get(number__iexact=self.kwargs["district_number"])
