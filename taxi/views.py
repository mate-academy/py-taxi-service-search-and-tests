from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import DriverForm, DriverLicenseUpdateForm, CarForm
from .models import Driver, Car, Manufacturer


def index(request):
    """View function for the home page of the site."""
    request.session["num_visits"] = request.session.get("num_visits", 0) + 1

    context = {
        "num_drivers": Driver.objects.count(),
        "num_cars": Car.objects.count(),
        "num_manufacturers": Manufacturer.objects.count(),
        "num_visits": request.session.get("num_visits")
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Manufacturer
    fields = "__all__"


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    paginate_by = 5


class ManufacturerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Manufacturer
    fields = "__all__"


class ManufacturerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Manufacturer
    success_url = reverse_lazy("taxi:manufacturer-list")


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.select_related("manufacturer")


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarForm


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car
    queryset = Car.objects.prefetch_related("drivers")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    form_class = DriverForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Driver
    form_class = DriverLicenseUpdateForm


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.prefetch_related("cars__manufacturer")


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")


@login_required
def add_remove_driver(request, pk):
    car = Car.objects.get(id=pk)
    if request.user in car.drivers.all():
        car.drivers.remove(request.user.pk)
    else:
        car.drivers.add(request.user.pk)
    return HttpResponseRedirect(
        reverse_lazy("taxi:car-detail", kwargs={"pk": pk})
    )
