from __future__ import annotations

from typing import Any

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Driver, Car, Manufacturer
from .forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
)

User = get_user_model()


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


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5

    def get_queryset(self) -> Any:
        queryset = super().get_queryset().order_by("name")
        self.search_form = ManufacturerSearchForm(self.request.GET)
        if self.search_form.is_valid():
            name = self.search_form.cleaned_data.get("name") or ""
            if name:
                queryset = queryset.filter(name__icontains=name)
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search_form"] = getattr(
            self, "search_form", ManufacturerSearchForm()
        )
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
    paginate_by = 5
    queryset = Car.objects.select_related("manufacturer")

    def get_queryset(self) -> Any:
        queryset = super().get_queryset().order_by("model")
        self.search_form = CarSearchForm(self.request.GET)
        if self.search_form.is_valid():
            model = self.search_form.cleaned_data.get("model") or ""
            if model:
                queryset = queryset.filter(model__icontains=model)
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search_form"] = getattr(self, "search_form", CarSearchForm())
        return context


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


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = User
    context_object_name = "driver_list"
    paginate_by = 5

    def get_queryset(self) -> Any:
        queryset = super().get_queryset().order_by("username")
        self.search_form = DriverSearchForm(self.request.GET)
        if self.search_form.is_valid():
            username = self.search_form.cleaned_data.get("username") or ""
            if username:
                queryset = queryset.filter(username__icontains=username)
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search_form"] = getattr(
            self,
            "search_form",
            DriverSearchForm(),
        )
        return context


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
    success_url = reverse_lazy("taxi:driver-list")


@login_required
def toggle_assign_to_car(request, pk):
    driver = Driver.objects.get(id=request.user.id)
    # NOTE: idealmente esta ação deveria ser POST-only para evitar mudanças
    # de estado via GET. Mantido aqui por compatibilidade com o projeto.
    if Car.objects.get(id=pk) in driver.cars.all():
        driver.cars.remove(pk)
    else:
        driver.cars.add(pk)
    return HttpResponseRedirect(reverse_lazy("taxi:car-detail", args=[pk]))
