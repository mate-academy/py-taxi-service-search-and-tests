from django.views import generic
from django.db.models import Q
from .models import Driver, Car, Manufacturer
from .forms import SearchForm

class ManufacturerListView(generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("search_query", "")
        context["search_form"] = SearchForm(initial={"search_query": search_query})
        return context

    def get_queryset(self):
        queryset = Manufacturer.objects.all()
        form = SearchForm(self.request.GET)
        if form.is_valid():
            # Search by name
            return queryset.filter(name__icontains=form.cleaned_data["search_query"])
        return queryset


class CarListView(generic.ListView):
    model = Car
    context_object_name = "car_list"
    template_name = "taxi/car_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("search_query", "")
        context["search_form"] = SearchForm(initial={"search_query": search_query})
        return context

    def get_queryset(self):
        queryset = Car.objects.select_related("manufacturer")
        form = SearchForm(self.request.GET)
        if form.is_valid():
            # Search by model
            return queryset.filter(model__icontains=form.cleaned_data["search_query"])
        return queryset


class DriverListView(generic.ListView):
    model = Driver
    context_object_name = "driver_list"
    template_name = "taxi/driver_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("search_query", "")
        context["search_form"] = SearchForm(initial={"search_query": search_query})
        return context

    def get_queryset(self):
        queryset = Driver.objects.all()
        form = SearchForm(self.request.GET)
        if form.is_valid():
            # Search by username
            return queryset.filter(username__icontains=form.cleaned_data["search_query"])
        return queryset
