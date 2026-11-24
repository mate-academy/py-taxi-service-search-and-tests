from taxi.forms import TitleSearchForm


class SearchMixin:
    search_field: str | None = None
    search_param = "title"

    def get_queryset(self):
        queryset = super().get_queryset()
        value = self.request.GET.get(self.search_param)

        if value and self.search_field:
            return queryset.filter(
                **{f"{self.search_field}__icontains": value}
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["search_form"] = TitleSearchForm(
            initial={
                self.search_param: self.request.GET.get(self.search_param, "")
            }
        )
        return context
