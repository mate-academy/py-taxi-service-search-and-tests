from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Driver, Car, Manufacturer
from .forms import DriverCreationForm, DriverLicenseUpdateForm, CarForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


# Index view (no search)
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
    }

    return render(request, "taxi/index.html", context=context)


# Manufacturer List View with Search
class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = Manufacturer.objects.all()
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query))
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


# Car Detail View
class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car
    template_name = "taxi/car_detail.html"
    context_object_name = "car"


# Car List View with Search
class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.select_related("manufacturer")
    template_name = "taxi/car_list.html"
    context_object_name = "car_list"

    def get_queryset(self):
        queryset = Car.objects.all()
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(Q(model__icontains=search_query))
        return queryset


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


# Driver List View with Search
class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5
    template_name = "taxi/driver_list.html"
    context_object_name = "driver_list"

    def get_queryset(self):
        queryset = Driver.objects.all()
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(Q(username__icontains=search_query))
        return queryset


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    template_name = "taxi/driver_detail.html"
    context_object_name = "driver"


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


# Function to toggle the assignment of a car
def toggle_assign_to_car(request, pk):
    car = Car.objects.get(pk=pk)
    car.is_assigned = not car.is_assigned  # Toggle the assignment status
    car.save()
    return redirect("taxi:car-list")
