from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import generic

from .forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    SearchForm,
)
from .models import Car, Manufacturer

User = get_user_model()


class SearchMixin:
    search_field = ""

    def get_queryset(self):
        queryset = super().get_queryset()
        self.search_form = SearchForm(self.request.GET)

        if self.search_form.is_valid():
            query = self.search_form.cleaned_data["query"]
            if query:
                queryset = queryset.filter(
                    **{f"{self.search_field}__icontains": query}
                )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = getattr(
            self,
            "search_form",
            SearchForm(self.request.GET),
        )
        return context


@login_required
def index(request):
    """View function for the home page of the site."""

    num_drivers = User.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()

    num_visits = request.session.get("num_visits", 0) + 1
    request.session["num_visits"] = num_visits

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits,
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(SearchMixin, LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    paginate_by = 5
    search_field = "name"


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


class CarListView(SearchMixin, LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    search_field = "model"

    def get_queryset(self):
        return super().get_queryset().select_related("manufacturer")


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


class DriverListView(SearchMixin, LoginRequiredMixin, generic.ListView):
    model = User
    paginate_by = 5
    search_field = "username"


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    queryset = User.objects.all().prefetch_related("cars__manufacturer")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = User
    form_class = DriverCreationForm


class DriverLicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = DriverLicenseUpdateForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy("taxi:driver-list")


@login_required
def toggle_assign_to_car(request, pk):
    driver = get_object_or_404(User, id=request.user.id)
    car = get_object_or_404(Car, id=pk)

    if car in driver.cars.all():
        driver.cars.remove(car)
    else:
        driver.cars.add(car)

    return HttpResponseRedirect(reverse_lazy("taxi:car-detail", args=[pk]))
