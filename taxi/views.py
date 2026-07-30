from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Driver, Car, Manufacturer
from .forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarForm,
    DriverUsernameSearchForm,
    ManufacturersNameSearchForm,
    CarModelSearchForm,
)


class SearchMixin:
    search_form_class = None
    search_field = None

    def get_search_form(self):
        return self.search_form_class(self.request.GET)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.get_search_form()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        form = self.get_search_form()

        if form.is_valid():
            value = form.cleaned_data.get(self.search_field)

            if value:
                queryset = queryset.filter(
                    **{f"{self.search_field}__icontains": value}
                )

        return queryset


@login_required
def index(request):
    """View function for the home page of the site."""

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


class ManufacturerListView(
    LoginRequiredMixin,
    SearchMixin,
    generic.ListView
):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5

    search_form_class = ManufacturersNameSearchForm
    search_field = "name"


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


class CarListView(
    LoginRequiredMixin,
    SearchMixin,
    generic.ListView
):
    model = Car
    paginate_by = 5
    queryset = Car.objects.select_related("manufacturer")

    search_form_class = CarModelSearchForm
    search_field = "model"


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")


class DriverListView(
    LoginRequiredMixin,
    SearchMixin,
    generic.ListView
):
    model = Driver
    paginate_by = 5

    search_form_class = DriverUsernameSearchForm
    search_field = "username"


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    form_class = DriverCreationForm


class DriverLicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Driver
    form_class = DriverLicenseUpdateForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("")


# Not my code, but okay, I changed it
@login_required
def toggle_assign_to_car(request, pk):
    driver = request.user
    car = get_object_or_404(Car, id=pk)

    if car in driver.cars.all():
        driver.cars.remove(car)
    else:
        driver.cars.add(car)

    return HttpResponseRedirect(
        reverse_lazy("taxi:car-detail", args=[pk])
    )
