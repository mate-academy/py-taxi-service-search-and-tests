from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import SearchForm
from .models import Car, Driver, Manufacturer


@login_required
def index(request):
    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits + 1,
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = Manufacturer.objects.order_by("name")
        form = SearchForm(self.request.GET)

        if form.is_valid():
            queryset = queryset.filter(
                name__icontains=form.cleaned_data["query"]
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query", "")
        context["search_form"] = SearchForm(initial={"query": query})
        return context


class ManufacturerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Manufacturer
    success_url = reverse_lazy("taxi:manufacturer-list")


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    context_object_name = "car_list"
    template_name = "taxi/car_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = Car.objects.select_related("manufacturer").order_by("model")
        form = SearchForm(self.request.GET)

        if form.is_valid():
            queryset = queryset.filter(
                model__icontains=form.cleaned_data["query"]
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query", "")
        context["search_form"] = SearchForm(initial={"query": query})
        return context


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car
    queryset = Car.objects.select_related(
        "manufacturer"
    ).prefetch_related("drivers")


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    fields = "__all__"
    success_url = reverse_lazy("taxi:car-list")


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    fields = "__all__"
    success_url = reverse_lazy("taxi:car-list")


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    context_object_name = "driver_list"
    template_name = "taxi/driver_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = Driver.objects.order_by("username")
        form = SearchForm(self.request.GET)

        if form.is_valid():
            queryset = queryset.filter(
                username__icontains=form.cleaned_data["query"]
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query", "")
        context["search_form"] = SearchForm(initial={"query": query})
        return context


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.prefetch_related("cars__manufacturer")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    fields = "__all__"
    success_url = reverse_lazy("taxi:driver-list")


class DriverUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Driver
    fields = "__all__"
    success_url = reverse_lazy("taxi:driver-list")


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")
