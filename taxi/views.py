from typing import Any
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from taxi.forms import (
    CarForm,
    CarSearchForm,
    DriverForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    ManufacturerSearchForm,
)

from .models import Driver, Car, Manufacturer


@login_required
def index(request: HttpRequest) -> HttpResponse:
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


class ManufacturerListView(LoginRequiredMixin, ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    paginate_by = 5

    def get_queryset(self) -> QuerySet[Manufacturer]:
        queryset = Manufacturer.objects.all()
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = ManufacturerSearchForm(initial={"name": name})
        return context


class CarListView(LoginRequiredMixin, ListView):
    model = Car
    paginate_by = 5

    def get_queryset(self) -> QuerySet[Car]:
        queryset = Car.objects.select_related("manufacturer")
        model = self.request.GET.get("model")
        if model:
            queryset = queryset.filter(model__icontains=model)
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        model = self.request.GET.get("model", "")
        context["search_form"] = CarSearchForm(initial={"model": model})
        return context


class CarDetailView(LoginRequiredMixin, DetailView):
    model = Car

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["driver_list"] = self.object.drivers.all()
        return context


class DriverListView(LoginRequiredMixin, ListView):
    model = Driver
    paginate_by = 5

    def get_queryset(self) -> QuerySet[Driver]:
        queryset = Driver.objects.all()
        username = self.request.GET.get("username")
        if username:
            queryset = queryset.filter(username__icontains=username)
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = DriverSearchForm(
            initial={"username": username}
        )
        return context


class DriverDetailView(LoginRequiredMixin, DetailView):
    model = Driver

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["car_list"] = self.object.cars.select_related("manufacturer")
        return context


class DriverCreateView(LoginRequiredMixin, CreateView):
    model = Driver
    form_class = DriverForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverDeleteView(LoginRequiredMixin, DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")
    context_object_name = "driver"
    template_name = "taxi/driver_delete.html"


class CarCreateView(LoginRequiredMixin, CreateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")
    context_object_name = "car"


class CarUpdateView(LoginRequiredMixin, UpdateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")
    context_object_name = "car"


class CarDeleteView(LoginRequiredMixin, DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")
    context_object_name = "car"
    template_name = "taxi/car_delete.html"


class ManufacturerCreateView(LoginRequiredMixin, CreateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")
    context_object_name = "manufacturer"


class ManufacturerUpdateView(LoginRequiredMixin, UpdateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")
    context_object_name = "manufacturer"


class ManufacturerDeleteView(LoginRequiredMixin, DeleteView):
    model = Manufacturer
    success_url = reverse_lazy("taxi:manufacturer-list")
    context_object_name = "manufacturer"
    template_name = "taxi/manufacturer_delete.html"


class CarDriverUpdateView(LoginRequiredMixin, View):
    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        user = request.user
        car = get_object_or_404(Car, pk=self.kwargs["pk"])
        if user in car.drivers.all():
            car.drivers.remove(user)
        else:
            car.drivers.add(user)
        return redirect("taxi:car-detail", pk=self.kwargs["pk"])


class DriverLicenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Driver
    form_class = DriverLicenseUpdateForm
    context_object_name = "driver"
    template_name = "taxi/driver_license_form.html"

    def get_success_url(self) -> str:
        return reverse_lazy(
            "taxi:driver-detail", kwargs={"pk": self.object.pk}
        )
