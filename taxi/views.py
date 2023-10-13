from django.contrib.auth.decorators import login_required
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
    SearchFieldForm,
)


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


class SearchFieldMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchFieldForm()
        context["search_form"].fields[
            "search_field"
        ].initial = self.request.GET.get("search_field")
        context["search_form"].fields["search_field"].widget.attrs[
            "placeholder"
        ] += self.placeholder
        return context

    def get_queryset(self):
        search_field = self.request.GET.get("search_field")

        if search_field:
            return self.model.objects.filter(**{self.lookup: search_field})
        return self.queryset


class ManufacturerListView(
    LoginRequiredMixin, SearchFieldMixin, generic.ListView
):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    queryset = Manufacturer.objects.all()  # I really need it here
    paginate_by = 5
    placeholder = "name"
    lookup = "name__icontains"


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


class CarListView(LoginRequiredMixin, SearchFieldMixin, generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.all().select_related("manufacturer")
    placeholder = "model"
    lookup = "model__icontains"


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


class DriverListView(LoginRequiredMixin, SearchFieldMixin, generic.ListView):
    model = Driver
    queryset = Driver.objects.all().prefetch_related(
        "cars__manufacturer"
    )  # I really need it here
    paginate_by = 5
    placeholder = "username"
    lookup = "username__icontains"


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
