from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import (
    DriverForm, DriverLicenseUpdateForm, CarForm, UniversalSearchForm
)
from .models import Driver, Car, Manufacturer


def index(request):
    """View function for the home page of the site."""
    request.session["num_visits"] = request.session.get("num_visits", 0) + 1
    context = {
        "num_drivers": Driver.objects.count(),
        "num_cars": Car.objects.count(),
        "num_manufacturers": Manufacturer.objects.count(),
        "num_visits": request.session.get("num_visits")
    }
    return render(request, "taxi/index.html", context=context)


class UniversalListView(generic.ListView):
    paginate_by = 5
    key_to_search = ""

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UniversalListView, self).get_context_data(**kwargs)
        context["search_form"] = UniversalSearchForm(initial={
            "field": self.request.GET.get("field", "")
        })
        return context

    def get_queryset(self):
        form = UniversalSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(**{
                f"{self.key_to_search}__icontains": form.cleaned_data["field"]
            })
        return self.queryset


class ManufacturerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Manufacturer
    fields = "__all__"


class ManufacturerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Manufacturer
    fields = "__all__"


class ManufacturerListView(LoginRequiredMixin, UniversalListView):
    queryset = Manufacturer.objects.all()
    key_to_search = "name"


class ManufacturerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Manufacturer
    success_url = reverse_lazy("taxi:manufacturer-list")


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm
    success_url = reverse_lazy("taxi:car-list")


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarForm


class CarListView(LoginRequiredMixin, UniversalListView):
    queryset = Car.objects.select_related("manufacturer")
    key_to_search = "model"


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    queryset = Car.objects.prefetch_related("drivers")


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    form_class = DriverForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Driver
    form_class = DriverLicenseUpdateForm


class DriverListView(LoginRequiredMixin, UniversalListView):
    queryset = Driver.objects.all()
    key_to_search = "username"


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    queryset = Driver.objects.prefetch_related("cars__manufacturer")


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")


@login_required
def add_remove_driver(request, pk):
    car = Car.objects.get(id=pk)
    if request.user in car.drivers.all():
        car.drivers.remove(request.user.pk)
    else:
        car.drivers.add(request.user.pk)
    return HttpResponseRedirect(
        reverse_lazy("taxi:car-detail", kwargs={"pk": pk})
    )
