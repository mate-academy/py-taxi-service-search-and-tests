from django.http import HttpRequest
from django.db.models.query import QuerySet


class SearchFormMixin:
    search_form_class = None
    search_param = None
    request: HttpRequest = None
    queryset: QuerySet = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_value = self.request.GET.get(self.search_param, "")

        context["search_form"] = self.search_form_class(initial={
            self.search_param: search_value
        })

        return context

    def get_queryset(self):
        form = self.search_form_class(self.request.GET)

        if form.is_valid():
            search_param_value = form.cleaned_data.get(self.search_param)
            filter_param = f"{self.search_param}__icontains"

            if search_param_value:
                return self.queryset.filter(
                    **{filter_param: search_param_value}
                )

        return self.queryset
