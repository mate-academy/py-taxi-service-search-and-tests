from http.client import HTTPResponse

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch, Q
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    ManufacturerSearchForm,
    CarSearchForm,
)
from taxi.models import Manufacturer, Car, Customer


Driver = get_user_model()


@login_required
def index(request):
    num_drivers = Driver.objects.all().count()
    num_manufacturers = Manufacturer.objects.all().count()
    num_cars = Car.objects.all().count()
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    context = {
        "num_drivers": num_drivers,
        "num_manufacturers": num_manufacturers,
        "num_cars": num_cars,
        "num_visits": request.session["num_visits"],
    }
    return render(request, "taxi/index.html", context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    template_name = "taxi/manufacturer_list.html"
    context_object_name = "manufacturer_list"
    queryset = Manufacturer.objects.order_by("name")
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ManufacturerListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["info"] = name
        context["search_form"] = ManufacturerSearchForm(
            initial={"name": name},
        )
        return context

    def get_queryset(self):
        queryset = Manufacturer.objects.all()
        form = ManufacturerSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data["name"]
            if name:
                return queryset.filter(name__icontains=name)
            # info = form.cleaned_data.get("info", "").strip()
            # if info:
            #     parts = info.split()
            #     if len(parts) == 1:
            #         return queryset.filter(
            #             Q(name__icontains=parts[0])
            #             | Q(country__icontains=parts[0])
            #         )
            #     if len(parts) >= 2:
            #         return queryset.filter(
            #             Q(name__icontains=parts[0])
            #             & Q(country__icontains=parts[1])
            #         )

        return queryset


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    template_name = "taxi/car_list.html"
    context_object_name = "car_list"
    queryset = Car.objects.select_related("manufacturer").order_by(
        "manufacturer__name"
    )
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(CarListView, self).get_context_data(**kwargs)
        model = self.request.GET.get("model", "")
        context["model"] = model
        context["search_form"] = CarSearchForm(
            initial={"model": model},
        )
        return context

    def get_queryset(self):
        queryset = Car.objects.select_related("manufacturer")
        form = CarSearchForm(self.request.GET)
        if form.is_valid():
            model = form.cleaned_data.get("model", "").strip()
            if model:
                return queryset.filter(model__icontains=model)

        return queryset


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    template_name = "taxi/driver_list.html"
    context_object_name = "driver_list"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(DriverListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["username"] = username
        context["search_form"] = DriverSearchForm(
            initial={"username": username},
        )
        return context

    def get_queryset(self):
        queryset = Driver.objects.prefetch_related("cars")
        form = DriverSearchForm(self.request.GET)
        print("FORM DATA:", self.request.GET)
        print("FORM IS VALID:", form.is_valid())
        print("FORM ERRORS:", form.errors)
        if form.is_valid():
            username = form.cleaned_data.get("username", "").strip()
            if username:
                return queryset.filter(username__icontains=username)

        return queryset


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")


def test_session_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Test Session</h1>")


class CustomerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Customer
    fields = "__all__"
    success_url = reverse_lazy("taxi:customer-list")
    template_name = "taxi/customer_form.html"


class CustomerListView(LoginRequiredMixin, generic.ListView):
    model = Customer
    template_name = "taxi/customer_list.html"
    context_object_name = "customer_list"


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    fields = "__all__"
    success_url = reverse_lazy("taxi:car-list")
    template_name = "taxi/car_form.html"


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    fields = "__all__"
    success_url = reverse_lazy("taxi:car-list")
    template_name = "taxi/car_confirm_delete.html"


class ManufacturerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")
    template_name = "taxi/manufacturer_form.html"


class ManufacturerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")
    template_name = "taxi/manufacturer_form.html"


class ManufacturerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")
    template_name = "taxi/manufacturer_confirm_delete.html"


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    form_class = DriverCreationForm


class DriverLicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Driver
    form_class = DriverLicenseUpdateForm


class DriverUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Driver
    form_class = DriverCreationForm


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")
    template_name = "taxi/driver_confirm_delete.html"


@login_required
def assign_to_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    user = request.user

    if user not in car.drivers.all():
        car.drivers.add(user)

    return redirect("taxi:car-detail", pk=car.pk)


def delete_assign_to_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    user = request.user

    if user in car.drivers.all():
        car.drivers.remove(user)

    return redirect("taxi:car-detail", pk=car.pk)
