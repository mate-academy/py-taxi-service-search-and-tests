from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model

from .models import Manufacturer, Car, Driver

User = get_user_model()


def index(request):
    return render(request, "taxi/index.html")


# Manufacturer views
class ManufacturerListView(ListView):
    model = Manufacturer
    template_name = "taxi/manufacturer_list.html"
    context_object_name = "manufacturers"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().order_by("pk")
        search_term = (self.request.GET.get("q") or "").strip()
        if search_term:
            qs = qs.filter(name__icontains=search_term)
        return qs


class ManufacturerCreateView(LoginRequiredMixin, CreateView):
    model = Manufacturer
    fields = ["name", "country"]
    template_name = "taxi/manufacturer_form.html"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerUpdateView(LoginRequiredMixin, UpdateView):
    model = Manufacturer
    fields = ["name", "country"]
    template_name = "taxi/manufacturer_form.html"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerDeleteView(LoginRequiredMixin, DeleteView):
    model = Manufacturer
    template_name = "taxi/manufacturer_confirm_delete.html"
    success_url = reverse_lazy("taxi:manufacturer-list")


# Car views
class CarListView(ListView):
    model = Car
    template_name = "taxi/car_list.html"
    context_object_name = "cars"
    paginate_by = 10

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .select_related("manufacturer")
            .prefetch_related("drivers")
            .order_by("pk")
        )
        search_term = (self.request.GET.get("q") or "").strip()
        if search_term:
            qs = qs.filter(
                Q(model__icontains=search_term)
                | Q(manufacturer__name__icontains=search_term)
            )
        return qs


class CarDetailView(DetailView):
    model = Car
    template_name = "taxi/car_detail.html"
    context_object_name = "car"


class CarCreateView(LoginRequiredMixin, CreateView):
    model = Car
    fields = ["model", "manufacturer", "drivers"]
    template_name = "taxi/car_form.html"
    success_url = reverse_lazy("taxi:car-list")


class CarUpdateView(LoginRequiredMixin, UpdateView):
    model = Car
    fields = ["model", "manufacturer", "drivers"]
    template_name = "taxi/car_form.html"
    success_url = reverse_lazy("taxi:car-list")


class CarDeleteView(LoginRequiredMixin, DeleteView):
    model = Car
    template_name = "taxi/car_confirm_delete.html"
    success_url = reverse_lazy("taxi:car-list")


# Driver views
class DriverListView(ListView):
    model = Driver
    template_name = "taxi/driver_list.html"
    context_object_name = "drivers"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().order_by("pk")
        search_term = (self.request.GET.get("q") or "").strip()
        if search_term:
            qs = qs.filter(
                Q(username__icontains=search_term)
                | Q(first_name__icontains=search_term)
                | Q(last_name__icontains=search_term)
            )
        return qs


class DriverDetailView(DetailView):
    model = Driver
    template_name = "taxi/driver_detail.html"
    context_object_name = "driver"


class DriverCreateView(LoginRequiredMixin, CreateView):
    model = Driver
    fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "license_number",
        "password",
    ]
    template_name = "taxi/driver_form.html"
    success_url = reverse_lazy("taxi:driver-list")


class DriverLicenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Driver
    fields = ["license_number"]
    template_name = "taxi/driver_form.html"
    success_url = reverse_lazy("taxi:driver-list")


class DriverDeleteView(LoginRequiredMixin, DeleteView):
    model = Driver
    template_name = "taxi/driver_confirm_delete.html"
    success_url = reverse_lazy("taxi:driver-list")


def _get_driver_for_user(user):
    if not user or not user.is_authenticated:
        return None

    if isinstance(user, Driver):
        return user

    drv = getattr(user, "driver", None)
    if isinstance(drv, Driver):
        return drv

    try:
        return Driver.objects.get(user=user)
    except (Driver.DoesNotExist, Driver.MultipleObjectsReturned):
        return None


def toggle_assign_to_car(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    car = get_object_or_404(Car, pk=pk)
    driver = _get_driver_for_user(request.user)
    if driver is None:
        return HttpResponseForbidden()

    if driver in car.drivers.all():
        car.drivers.remove(driver)
    else:
        car.drivers.add(driver)

    return redirect(reverse("taxi:car-detail", kwargs={"pk": pk}))
