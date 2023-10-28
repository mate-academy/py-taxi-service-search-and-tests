from django.db.models import QuerySet


class ListSearchMixin:
    search_form = None
    search_field_name = "search_input"
    filter_field = None

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(object_list=None, **kwargs)

        initial_data = self.request.GET.get(self.search_field_name, "")
        form = self.search_form(initial={self.search_field_name: initial_data})

        context["search_form"] = form

        return context

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()

        search_input_data = self.request.GET.get(self.search_field_name)
        if search_input_data:
            return queryset.filter(**{self.filter_field: search_input_data})
        return queryset
