from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q

from .forms import CarForm, DriverCreationForm, DriverLicenseUpdateForm
from .models import Car, Manufacturer

UserModel = get_user_model()


def index(request):
    num_visits = request.session.get("num_visits", 0) + 1
    request.session["num_visits"] = num_visits
    context = {
        "num_visits": num_visits,
        "num_cars": Car.objects.count(),
        "num_manufacturers": Manufacturer.objects.count(),
        "num_drivers": UserModel.objects.count(),
    }
    return render(request, "taxi/index.html", context)


# -------------------------------
# Manufacturer Views (ADICIONADA)
# -------------------------------
class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"

    def get_queryset(self):
        queryset = Manufacturer.objects.all()
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset


# -------------------------------
# Car Views
# -------------------------------
class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    context_object_name = "car_list"
    queryset = Car.objects.select_related("manufacturer").prefetch_related("drivers")

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(model__icontains=search)
        return queryset


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car
    context_object_name = "car"

    def post(self, request, *args, **kwargs):
        """
        Toggle assignment: se o usuário já está na lista de drivers do carro,
        remove; caso contrário, adiciona. Retorna redirect para a mesma página.
        """
        car = self.get_object()
        user = request.user
        if user in car.drivers.all():
            car.drivers.remove(user)
        else:
            car.drivers.add(user)
        return redirect("taxi:car-detail", pk=car.pk)


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


# -------------------------------
# Driver Views (use UserModel)
# -------------------------------
class DriverListView(LoginRequiredMixin, generic.ListView):
    model = UserModel
    context_object_name = "driver_list"

    def get_queryset(self):
        queryset = UserModel.objects.all()
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(username__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        for driver in context["driver_list"]:
            driver.is_current_user = (driver == current_user)
        return context


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = UserModel
    context_object_name = "driver"


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = UserModel
    form_class = DriverCreationForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverLicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = UserModel
    form_class = DriverLicenseUpdateForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = UserModel
    success_url = reverse_lazy("taxi:driver-list")
