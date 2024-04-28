from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic


from taxi.forms import (CarForm, CarSearchForm,
                        DriverCreationForm,
                        DriverLicenseUpdateForm,
                        ManufacturerSearchForm,
                        DriverSearchForm)
from taxi.models import Manufacturer, Car

User_model = get_user_model()


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_cars = Car.objects.count()
    num_drivers = User_model.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {"num_cars": num_cars,
               "num_drivers": num_drivers,
               "num_manufacturers": num_manufacturers,
               "num_visits": request.session["num_visits"]}
    return render(request, template_name="taxi/index.html", context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        manufactur_name = self.request.GET.get("manufactur_name", "")
        manufacture_country = self.request.GET.get("manufacture_country", "")
        context["search_form"] = ManufacturerSearchForm(
            initial={"manufactur_name": manufactur_name,
                     "manufacture_country": manufacture_country}
        )

        return context

    def get_queryset(self):
        self.queryset = Manufacturer.objects.all()
        form = ManufacturerSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["manufactur_name"],
                country__icontains=form.cleaned_data["manufacture_country"],
            )
        return self.queryset


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        car_model = self.request.GET.get("car_model", "")
        car_manufacture = self.request.GET.get("car_manufacture", "")
        context["search_form"] = CarSearchForm(
            initial={"car_model": car_model,
                     "car_manufacture": car_manufacture}
        )

        return context

    def get_queryset(self):
        self.queryset = Car.objects.select_related("manufacturer")
        form = CarSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                model__icontains=form.cleaned_data["car_model"],
                manufacturer__name__icontains=(
                    form.cleaned_data["car_manufacture"]
                ),
            )
        return self.queryset


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = User_model
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        driver_name = self.request.GET.get("driver_name", "")
        context["search_form"] = DriverSearchForm(
            initial={"driver_name": driver_name})
        return context

    def get_queryset(self):
        self.queryset = User_model.objects.all()
        driver_search = self.request.GET.get("driver_name")
        if driver_search:
            return self.queryset.filter(
                Q(first_name__icontains=driver_search)
                | Q(last_name__icontains=driver_search)
            )
        return self.queryset


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = User_model
    queryset = User_model.objects.prefetch_related("cars__drivers")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = User_model
    form_class = DriverCreationForm


class DriverLisenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User_model
    form_class = DriverLicenseUpdateForm


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User_model
    success_url = reverse_lazy("taxi:driver-list")
    template_name = "taxi/drivers_confirm_delete.html"


class CarsCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")
    template_name = "taxi/cars_form.html"


class CarsUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    fields = "__all__"
    success_url = reverse_lazy("taxi:car-list")
    template_name = "taxi/cars_form.html"


class CarsDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")
    template_name = "taxi/cars_confirm_delete.html"


@login_required
def toggle_assign_to_car(request, pk) -> HttpResponseRedirect:
    driver = User_model.objects.get(id=request.user.id)
    if Car.objects.get(id=pk) in driver.cars.all():
        driver.cars.remove(pk)
    else:
        driver.cars.add(pk)
    return HttpResponseRedirect(reverse_lazy("taxi:car-detail", args=[pk]))


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
    success_url = reverse_lazy("taxi:manufacturer-list")
    template_name = "taxi/manufacturer_confirm_delete.html"
