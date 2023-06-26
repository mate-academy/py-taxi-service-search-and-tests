from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormMixin
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from sweetify.views import SweetifySuccessMixin

from .models import Driver, Car, Manufacturer, CarComments
from .forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    CarForm,
    ManufacturerSearchForm,
    CarSearchForm,
    DriverSearchForm,
    CarCommentForm,
    DriverSettingsForm,
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
    queryset = Manufacturer.objects.all()
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ManufacturerListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = ManufacturerSearchForm(initial={"name": name})

        return context

    def get_queryset(self):
        form = ManufacturerSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return self.queryset


class ManufacturerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Manufacturer


class ManufacturerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")


class ManufacturerUpdateView(LoginRequiredMixin, SweetifySuccessMixin, generic.UpdateView):
    model = Manufacturer
    fields = "__all__"
    success_url = reverse_lazy("taxi:manufacturer-list")
    success_message = "Manufacturer successfully update"


class ManufacturerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Manufacturer
    success_url = reverse_lazy("taxi:manufacturer-list")


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 4
    queryset = Car.objects.all().select_related("manufacturer")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CarListView, self).get_context_data(**kwargs)
        model = self.request.GET.get("model", "")
        context["search_form"] = CarSearchForm(initial={"model": model})

        return context

    def get_queryset(self):
        form = CarSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                model__icontains=form.cleaned_data["model"]
            )
        return self.queryset


class CarDetailView(LoginRequiredMixin, FormMixin, generic.DetailView):
    model = Car
    form_class = CarCommentForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid:
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            "taxi:car-detail", kwargs={"pk": self.get_object().id}
        )

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.car = self.get_object()
        self.object.driver = self.request.user
        self.object.save()
        return super().form_valid(form)


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
    paginate_by = 4
    queryset = Driver.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DriverListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username")
        context["search_form"] = DriverSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        form = DriverSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return self.queryset


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    form_class = DriverCreationForm
    success_url = reverse_lazy("taxi:driver-list")


class DriverLicenseUpdateView(LoginRequiredMixin, SweetifySuccessMixin, generic.UpdateView):
    model = Driver
    form_class = DriverLicenseUpdateForm
    success_url = reverse_lazy("taxi:driver-list")
    success_message = "License successfully update"

    def get(self, request, *args, **kwargs):
        driver = self.get_object()
        if not request.user.is_staff:
            if request.user.id == driver.id:
                return super().get(request, *args, **kwargs)
        if request.user.is_staff:
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect("/")

    def get_success_url(self, **kwargs):
        return reverse_lazy("taxi:driver-detail", kwargs={"pk": self.get_object().id})


class DriverDeleteView(LoginRequiredMixin, SweetifySuccessMixin, generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:driver-list")
    permission_required = "taxi.delete-driver"
    success_message = "User deleted successfully"


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


class RegistrationView(generic.CreateView):
    model = get_user_model()
    form_class = DriverCreationForm
    template_name = "taxi/registration.html"
    success_url = reverse_lazy("taxi:registration-complete")


def registration_complete(request):
    return render(request, "registration/register.html")


class CommentDeleteView(SweetifySuccessMixin, generic.DeleteView):
    model = CarComments
    success_url = reverse_lazy("taxi:car-list")
    success_message = "Comment successfully deleted"

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            "taxi:car-detail", kwargs={"pk": self.get_object().car.id}
        )

    def get(self, request, *args, **kwargs):
        comment = self.get_object().driver.id
        if not request.user.is_staff:
            if request.user.id == comment:
                return super(CommentDeleteView, self).get(
                    request, *args, **kwargs
                )
        if request.user.is_staff:
            return super(CommentDeleteView, self).get(request, *args, **kwargs)
        return HttpResponseRedirect("/")


class DriverSettingsView(
    LoginRequiredMixin, SweetifySuccessMixin, generic.UpdateView
):
    model = get_user_model()
    form_class = DriverSettingsForm
    success_url = reverse_lazy("taxi:driver-list")
    success_message = "Settings updated"

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            "taxi:driver-detail", kwargs={"pk": self.get_object().id}
        )

    def get(self, request, *args, **kwargs):
        driver = self.get_object()
        if not request.user.is_staff:
            if request.user.id == driver.id:
                return super(DriverSettingsView, self).get(
                    request, *args, **kwargs
                )
        if request.user.is_staff:
            return super(DriverSettingsView, self).get(
                request, *args, **kwargs
            )
        return HttpResponseRedirect("/")


def like_and_unlike(request, id, pk):  # noqa
    comment = get_object_or_404(
        CarComments, id=request.POST.get("car.comment.id"), pk=pk
    )
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return HttpResponseRedirect(reverse("taxi:car-detail", args=[str(id)]))
