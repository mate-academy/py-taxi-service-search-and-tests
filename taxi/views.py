from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import CarForm, DriverCreationForm, DriverLicenseUpdateForm
from .models import Car, Driver, Manufacturer


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context: dict[str, int] = {
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

    def get_queryset(self) -> QuerySet[Manufacturer]:
        queryset = Manufacturer.objects.all().order_by("id")
        name = self.request.GET.get("name")

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


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
    paginate_by = 5

    def get_queryset(self) -> QuerySet[Car]:
        queryset = Car.objects.select_related("manufacturer").order_by("id")
        model = self.request.GET.get("model")

        if model:
            queryset = queryset.filter(model__icontains=model)

        return queryset


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
    model = Driver
    paginate_by = 5

    def get_queryset(self) -> QuerySet[Driver]:
        queryset = Driver.objects.all().order_by("id")
        username = self.request.GET.get("username")

        if username:
            queryset = queryset.filter(username__icontains=username)

        return queryset


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
def toggle_assign_to_car(
    request: HttpRequest,
    pk: int,
) -> HttpResponseRedirect:
    driver = Driver.objects.get(id=request.user.id)
    car = Car.objects.get(id=pk)

    if car in driver.cars.all():
        driver.cars.remove(pk)
    else:
        driver.cars.add(pk)

    return HttpResponseRedirect(reverse_lazy("taxi:car-detail", args=[pk]))
