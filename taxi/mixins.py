class SearchMixin:
    search_form_class = None
    search_field = None

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.search_form_class and self.search_field:
            form = self.search_form_class(self.request.GET)

            if form.is_valid():
                search_value = form.cleaned_data.get(self.search_field, "")
                if search_value:
                    filter_kwargs = {
                        f"{self.search_field}__icontains": search_value}
                    return queryset.filter(**filter_kwargs)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_value = self.request.GET.get(self.search_field, "")
        if self.search_form_class and self.search_field:
            context["search_form"] = self.search_form_class(
                initial={self.search_field: search_value})

        return context
