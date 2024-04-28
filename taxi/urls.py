from django.urls import path

from taxi.views import (
    index,
    CarListView,
    CarDetailView,
    CarsCreateView,
    CarsUpdateView,
    CarsDeleteView,
    DriverListView,
    DriverCreateView,
    DriverDeleteView,
    DriverDetailView,
    DriverLisenseUpdateView,
    ManufacturerListView,
    ManufacturerCreateView,
    ManufacturerUpdateView,
    ManufacturerDeleteView,
    toggle_assign_to_car
)

urlpatterns = [
    path("", index, name="index"),

    path("drivers/", DriverListView.as_view(), name="driver-list"),
    path("drivers/<int:pk>/",
         DriverDetailView.as_view(),
         name="driver-detail"),
    path("drivers/create/", DriverCreateView.as_view(), name="driver-create"),
    path("drivers/<int:pk>/lisence_update/",
         DriverLisenseUpdateView.as_view(),
         name="driver-update"),
    path("drivers/<int:pk>/delete/",
         DriverDeleteView.as_view(),
         name="driver-delete"),

    path("cars/", CarListView.as_view(), name="car-list"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("cars/create/", CarsCreateView.as_view(), name="car-create"),
    path("cars/<int:pk>/update/",
         CarsUpdateView.as_view(),
         name="car-update"),
    path("cars/<int:pk>/delete/",
         CarsDeleteView.as_view(),
         name="car-delete"),
    path("cars/<int:pk>/toggle-assign/",
         toggle_assign_to_car,
         name="toggle-car-assign",),

    path("manufacturers/",
         ManufacturerListView.as_view(),
         name="manufacturer-list"),
    path("manufacturers/create/",
         ManufacturerCreateView.as_view(),
         name="manufacturer-create"),
    path("manufacturers/<int:pk>/update/",
         ManufacturerUpdateView.as_view(),
         name="manufacturer-update"),
    path("manufacturers/<int:pk>/delete/",
         ManufacturerDeleteView.as_view(),
         name="manufacturer-delete"),
]

app_name = "taxi"
