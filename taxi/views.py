from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View, generic
from django.views.generic import TemplateView

from taxi.forms import (
    CarCreationForm,
    CustomDriverCreationForm,
    DriverLicenseUpdateForm,
    SingleFieldSearchForm,
)
from taxi.models import Car, Driver, Manufacturer


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "taxi/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        num_visits = self.request.session.get("num_visits", 0) + 1
        self.request.session["num_visits"] = num_visits

        context["num_cars"] = Car.objects.count()
        context["num_drivers"] = get_user_model().objects.count()
        context["num_manufacturers"] = Manufacturer.objects.count()
        context["num_visits"] = num_visits
        return context


class ManufacturerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Manufacturer
    fields = ("name", "country")

    def get_success_url(self):
        return (self.request.GET.get("back")
                or reverse("taxi:manufacturer-list"))


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query", "")
        context["search_form"] = SingleFieldSearchForm(
            initial={"query": query}
        )
        return context

    def get_queryset(self):
        queryset = self.model.objects.all()
        form = SingleFieldSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["query"]
            )
        return queryset


class ManufacturerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Manufacturer


class ManufacturerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Manufacturer
    fields = ("name", "country")

    def get_success_url(self):
        return self.request.GET.get("back")


class ManufacturerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Manufacturer

    def get_success_url(self):
        return (self.request.GET.get("back")
                or reverse_lazy("taxi:manufacturer-list"))


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarCreationForm
    success_url = reverse_lazy("taxi:car-list")


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query", "")
        context["search_form"] = SingleFieldSearchForm(
            initial={"query": query}
        )
        return context

    def get_queryset(self):
        queryset = self.model.objects.select_related("manufacturer")
        form = SingleFieldSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(
                model__icontains=form.cleaned_data["query"]
            )
        return queryset.order_by("id")


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class AssignCarView(LoginRequiredMixin, View):
    def get(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        return render(request, "taxi/assign_confirm.html", {"car": car})

    def post(self, request, pk):
        car = get_object_or_404(Car, pk=pk)
        action = request.POST.get("assign")

        action_map = {
            "update": car.drivers.add,
            "remove": car.drivers.remove
        }

        if action in action_map:
            action_map[action](request.user)

        return redirect("taxi:car-detail", pk=pk)


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarCreationForm

    def get_success_url(self):
        return reverse_lazy("taxi:car-detail", kwargs={"pk": self.object.id})


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:car-list")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = CustomDriverCreationForm
    template_name = "taxi/driver_form.html"
    success_url = reverse_lazy("taxi:driver-list")


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("query", "")
        context["search_form"] = SingleFieldSearchForm(
            initial={"query": query}
        )
        return context

    def get_queryset(self):
        queryset = get_user_model().objects.all()
        form = SingleFieldSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["query"]
            )
        return queryset


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver

    def get_queryset(self) -> QuerySet:
        return self.model.objects.prefetch_related("cars__manufacturer")


class DriverUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Driver

    def get_form_class(self):
        form_license = self.request.GET.get("form_license")
        if form_license == "upd_license":
            return DriverLicenseUpdateForm
        return CustomDriverCreationForm

    def get_success_url(self):
        return reverse("taxi:driver-detail", kwargs={"pk": self.object.pk})


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")
