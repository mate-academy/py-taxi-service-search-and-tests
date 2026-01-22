from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Driver, Car, Manufacturer
from .forms import DriverCreationForm, DriverLicenseUpdateForm, CarForm


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
    return render(request, "taxi/index.html",
                  context=context)


class BaseListView(LoginRequiredMixin,
                   generic.ListView):
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(self.get_search_filter(query))
        print(queryset)
        return queryset

    def get_search_filter(self, query):
        raise NotImplementedError("Override this method in child classes")


class DriverListView(BaseListView):
    model = Driver
    context_object_name = "driver_list"
    template_name = "taxi/driver_list.html"
    paginate_by = 10
    ordering = ["username"]

    def get_search_filter(self, query):
        return Q(username__icontains=query)


class CarListView(BaseListView):
    model = Car
    queryset = Car.objects.select_related("manufacturer")
    template_name = "taxi/car_list.html"

    def get_search_filter(self, query):
        return Q(model__icontains=query)


def get_search_filter(query):
    return Q(name__icontains=query)


class ManufacturerListView(ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 10
    ordering = ["name"]

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(get_search_filter(query))
        return queryset


class BaseCreateUpdateDeleteView(LoginRequiredMixin):
    model = None
    form_class = None
    success_url = None
    template_name_suffix = None


class ManufacturerCreateView(BaseCreateUpdateDeleteView,
                             generic.CreateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerUpdateView(BaseCreateUpdateDeleteView,
                             generic.UpdateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerDeleteView(BaseCreateUpdateDeleteView,
                             generic.DeleteView):
    model = Manufacturer
    success_url = reverse_lazy("taxi:manufacturer-list")


class CarCreateView(BaseCreateUpdateDeleteView,
                    generic.CreateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarUpdateView(BaseCreateUpdateDeleteView,
                    generic.UpdateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarDeleteView(BaseCreateUpdateDeleteView,
                    generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")


class DriverCreateView(BaseCreateUpdateDeleteView,
                       generic.CreateView):
    model = Driver
    form_class = DriverCreationForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverLicenseUpdateView(BaseCreateUpdateDeleteView,
                              generic.UpdateView):
    model = Driver
    form_class = DriverLicenseUpdateForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverDetailView(LoginRequiredMixin,
                       generic.DetailView):
    model = Driver
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")


class CarDetailView(LoginRequiredMixin,
                    generic.DetailView):
    """View to display details of a car."""
    model = Car
    template_name = "taxi/car_detail.html"


class DriverDeleteView(LoginRequiredMixin,
                       generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")


@login_required
def toggle_assign_to_car(request, pk):
    """Toggle assignment of a car to a driver."""
    driver = Driver.objects.get(id=request.user.id)
    car = get_object_or_404(Car, id=pk)

    if car in driver.cars.all():
        driver.cars.remove(car)
    else:
        driver.cars.add(car)

    return HttpResponseRedirect(reverse_lazy("taxi:driver-list"))
