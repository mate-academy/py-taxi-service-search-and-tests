from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Driver, Car, Manufacturer
from .forms import (
    DriverCreationForm, DriverLicenseUpdateForm, CarForm,
    SearchListForm
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


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturer_list"
    template_name = "taxi/manufacturer_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        search = self.request.GET.get("search", "")
        context["form_search"] = SearchListForm(initial={"search": search})
        return context

    def get_queryset(self):
        search_form = SearchListForm(data=self.request.GET)
        queryset = super().get_queryset()
        if search_form.is_valid():
            queryset = queryset.filter(
                Q(name__icontains=search_form.cleaned_data.get("search"))
                | Q(country__icontains=search_form.cleaned_data.get("search"))
            )
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        search = self.request.GET.get("search", "")
        context["form_search"] = SearchListForm(initial={"search": search})
        return context

    def get_queryset(self):
        search_form = SearchListForm(data=self.request.GET)
        queryset = Car.objects.all().select_related("manufacturer")
        if search_form.is_valid():
            queryset = queryset.filter(
                Q(model__icontains=search_form.cleaned_data.get("search"))
                | Q(
                    manufacturer__name__icontains=search_form.cleaned_data.get(
                        "search"
                    )
                )
            )
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        search = self.request.GET.get("search", "")
        context["form_search"] = SearchListForm(initial={"search": search})
        return context

    def get_queryset(self):
        search_form = SearchListForm(data=self.request.GET)
        queryset = super().get_queryset()
        if search_form.is_valid():
            queryset = queryset.filter(
                Q(first_name__icontains=search_form.cleaned_data.get("search"))
                | Q(
                    last_name__icontains=search_form.cleaned_data.get("search")
                ) | Q(license_number=search_form.cleaned_data.get("search"))
            )
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
def toggle_assign_to_car(request, pk):
    driver = Driver.objects.get(id=request.user.id)
    if (
            Car.objects.get(id=pk) in driver.cars.all()
    ):  # probably could check if car exists
        driver.cars.remove(pk)
    else:
        driver.cars.add(pk)
    return HttpResponseRedirect(reverse_lazy("taxi:car-detail", args=[pk]))
