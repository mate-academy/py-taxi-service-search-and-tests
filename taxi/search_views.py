from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Driver, Car, Manufacturer


class DriverSearchView(ListView):
    model = Driver
    template_name = "taxi/driver_search.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Driver.objects.filter(username__icontains=query) \
            if query else Driver.objects.all()


class CarSearchView(ListView):
    model = Car
    template_name = "taxi/car_search.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Car.objects.filter(model__icontains=query) \
            if query else Car.objects.all()


class ManufacturerSearchView(ListView):
    model = Manufacturer
    template_name = "taxi/manufacturer_search.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        return Manufacturer.objects.filter(name__icontains=query) \
            if query else Manufacturer.objects.all()
