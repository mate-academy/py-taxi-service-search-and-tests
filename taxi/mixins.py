class SearchMixin:
    search_fields = []
    search_form_class = None

    def get_search_form(self):
        return self.search_form_class(self.request.GET)

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.get_search_form()
        if form.is_valid():
            for field in self.search_fields:
                value = form.cleaned_data.get(field)
                if value:
                    queryset = queryset.filter(
                        **{f"{field}__icontains": value}
                    )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.get_search_form()
        return context
