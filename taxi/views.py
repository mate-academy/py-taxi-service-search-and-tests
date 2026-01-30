from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Driver, Car, Manufacturer

# ... (outras views que você já tem)

class DriverListView(LoginRequiredMixin, ListView):
    model = Driver
    template_name = "taxi/driver_list.html"
    context_object_name = "drivers"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get("q")
        if search_term:
            queryset = queryset.filter(username__icontains=search_term)
        return queryset


class CarListView(LoginRequiredMixin, ListView):
    model = Car
    template_name = "taxi/car_list.html"
    context_object_name = "cars"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get("q")
        if search_term:
            queryset = queryset.filter(model__icontains=search_term)
        return queryset


class ManufacturerListView(LoginRequiredMixin, ListView):
    model = Manufacturer
    template_name = "taxi/manufacturer_list.html"
    context_object_name = "manufacturers"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.GET.get("q")
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)
        return queryset

