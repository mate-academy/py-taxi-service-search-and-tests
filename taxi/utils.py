from .forms import SearchForm


class SearchMixin:
    search_field = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("search_query", "")
        context["search_form"] = SearchForm(
            search_by=self.search_field,
            initial={"search_query": search_query})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = SearchForm(self.search_field, self.request.GET)
        if form.is_valid():
            search_query = form.cleaned_data["search_query"]
            if search_query:
                filter_criteria = {
                    f"{self.search_field}__icontains": search_query
                }
                queryset = queryset.filter(**filter_criteria)
        return queryset
