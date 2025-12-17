from django.views import generic
from django.db.models import Q


class SearchableListView(generic.ListView):

    search_form_class = None
    search_fields = None

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.search_form_class or not self.search_fields:
            return queryset

        form = self.search_form_class(self.request.GET)
        if form.is_valid():
            search_term = form.cleaned_data.get("search_term", "")
            if search_term:
                query = Q()
                for field in self.search_fields:
                    query |= Q(**{f"{field}__icontains": search_term})

                queryset = queryset.filter(query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.search_form_class:
            context["search_form"] = self.search_form_class(
                initial={"search_term": self.request.GET.get(
                    "search_term",
                    ""
                )}
            )

        return context
