from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme

from .models import Driver, Car, Manufacturer
from .forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
)


@login_required
def index(request):
    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    visits = request.session.get("num_visits", 0) + 1
    request.session["num_visits"] = visits

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": visits,
    }
    return render(request, "taxi/index.html", context)


# ---------- Manufacturers ----------
class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = Manufacturer.objects.all()
        form = ManufacturerSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get("name") or ""
            if name:
                queryset = queryset.filter(name__icontains=name)
        return queryset

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search_form"] = ManufacturerSearchForm(self.request.GET)
        return ctx


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


# ---------- Cars ----------
class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    context_object_name = "car_list"
    paginate_by = 5
    queryset = (Car.objects.select_related("manufacturer").
                prefetch_related("drivers"))

    def get_queryset(self):
        queryset = super().get_queryset()
        form = CarSearchForm(self.request.GET)
        if form.is_valid():
            model = form.cleaned_data.get("model") or ""
            if model:
                queryset = queryset.filter(model__icontains=model)
        return queryset

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search_form"] = CarSearchForm(self.request.GET)
        return ctx


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car
    queryset = (Car.objects.select_related("manufacturer")
                .prefetch_related("drivers"))


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


# ---------- Drivers ----------
class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    context_object_name = "driver_list"
    paginate_by = 5

    def get_queryset(self):
        queryset = Driver.objects.all()
        form = DriverSearchForm(self.request.GET)
        if form.is_valid():
            username = form.cleaned_data.get("username") or ""
            if username:
                queryset = queryset.filter(username__icontains=username)
        return queryset

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search_form"] = DriverSearchForm(self.request.GET)
        return ctx


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.prefetch_related("cars__manufacturer")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    form_class = DriverCreationForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverLicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Driver
    form_class = DriverLicenseUpdateForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")


@require_POST
@login_required
def toggle_assign_to_car(request, pk):
    driver = request.user
    car = get_object_or_404(Car, pk=pk)

    if driver.cars.filter(pk=car.pk).exists():
        driver.cars.remove(car)
    else:
        driver.cars.add(car)

    next_url = request.GET.get("next")
    if next_url and url_has_allowed_host_and_scheme(
            next_url,
            {request.get_host()}
    ):
        return HttpResponseRedirect(next_url)
    return HttpResponseRedirect(reverse_lazy("taxi:car-detail", args=[pk]))
