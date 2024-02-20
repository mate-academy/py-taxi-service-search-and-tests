from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Driver, Car, Manufacturer
from .forms import (
    CarForm,
    CarSearchForm,
    DriverSearchForm,
    DriverCreationForm,
    ManufacturerSearchForm,
    DriverLicenseUpdateForm,
)


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
        "url_home": True
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    extra_context = {"url_manufacturer": True}
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ManufacturerListView, self).get_context_data(**kwargs)
        context["search_form"] = ManufacturerSearchForm(
            initial={"name": self.request.GET.get("name")}
        )

        return context

    def get_queryset(self):
        queryset = Manufacturer.objects.all()
        name = self.request.GET.get("name")

        if name:
            return queryset.filter(name__icontains=name)

        return queryset


class ManufacturerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Manufacturer
    extra_context = {"url_manufacturer": True}
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Manufacturer
    extra_context = {"url_manufacturer": True}
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Manufacturer
    extra_context = {"url_manufacturer": True}
    success_url = reverse_lazy("taxi:manufacturer-list")


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    extra_context = {"url_car": True}
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CarListView, self).get_context_data(**kwargs)
        context["search_form"] = CarSearchForm(
            initial={"model": self.request.GET.get("model")}
        )

        return context

    def get_queryset(self):
        queryset = Car.objects.select_related("manufacturer")
        model = self.request.GET.get("model")

        if model:
            return queryset.filter(model__icontains=model)

        return queryset


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car
    extra_context = {"url_car": True}


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    extra_context = {"url_car": True}
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    extra_context = {"url_car": True}
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    extra_context = {"url_car": True}
    success_url = reverse_lazy("taxi:car-list")


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    extra_context = {"url_driver": True}
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DriverListView, self).get_context_data(**kwargs)
        context["search_form"] = DriverSearchForm(
            initial={"username": self.request.GET.get("username")}
        )

        return context

    def get_queryset(self):
        queryset = Driver.objects.all()
        username = self.request.GET.get("username")

        if username:
            return queryset.filter(username__icontains=username)

        return queryset


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    extra_context = {"url_driver": True}
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    extra_context = {"url_driver": True}
    form_class = DriverCreationForm


class DriverLicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Driver
    extra_context = {"url_driver": True}
    form_class = DriverLicenseUpdateForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    extra_context = {"url_driver": True}
    success_url = reverse_lazy("")


@login_required
def toggle_assign_to_car(request, pk):
    driver = Driver.objects.get(id=request.user.id)
    if (
        Car.objects.get(id=pk) in driver.cars.all()
    ):  # probably could check if car exists
        driver.cars.remove(pk)
    else:
        driver.cars.add(pk)
    return HttpResponseRedirect(reverse_lazy("taxi:car-detail", args=[pk]))
