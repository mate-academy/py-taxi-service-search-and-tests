from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Driver, Car, Manufacturer
from .forms import DriverCreationForm, DriverLicenseUpdateForm, CarForm
from django.db.models import Q
from .forms import CarSearchForm, DriverSearchForm, ManufacturerSearchForm


def car_search_view(request):
    form = CarSearchForm(request.GET or None)
    cars = Car.objects.all()

    if form.is_valid():
        model = form.cleaned_data.get("model")
        if model:
            cars = cars.filter(model__icontains=model)

    return render(request, "taxi/car_list.html", {"form": form, "cars": cars})


def driver_search_view(request):
    form = DriverSearchForm(request.GET or None)
    drivers = Driver.objects.all()

    if form.is_valid():
        username = form.cleaned_data.get("username")
        if username:
            drivers = drivers.filter(username__icontains=username)

    return render(
        request, "taxi/driver_list.html",
        {"form": form, "drivers": drivers}
    )


def manufacturer_search_view(request):
    form = ManufacturerSearchForm(request.GET or None)
    manufacturers = Manufacturer.objects.all()

    if form.is_valid():
        name = form.cleaned_data.get("name")
        if name:
            manufacturers = manufacturers.filter(name__icontains=name)

    return render(
        request, "taxi/manufacturer_list.html",
        {"form": form, "manufacturers": manufacturers}
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


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.select_related("manufacturer")

    # Переопределяем метод get_queryset для фильтрации данных
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(
                Q(model__icontains=search_query)
            )
        return queryset

    # Передаем форму в контекст для использования в шаблоне
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CarSearchForm(self.request.GET or None)
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
    model = Driver
    paginate_by = 5

    # Переопределяем метод для фильтрации по имени пользователя
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query)
            )
        return queryset

    # Передаем форму в контекст для использования в шаблоне
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = DriverSearchForm(self.request.GET or None)
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
