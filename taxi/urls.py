from django.urls import path

from taxi.views import (
    IndexView,
    ManufacturerListView,
    ManufacturerDetailView,
    CarListView,
    CarDetailView,
    CarCreateView,
    CarUpdateView,
    CarDeleteView,
    DriverListView,
    DriverDetailView,
    DriverCreateView,
    DriverDeleteView,
    DriverLicenseUpdateView,
    assign_me_to_car,
    delete_me_from_car,
)

app_name = "taxi"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),

    path(
        "manufacturers/",
        ManufacturerListView.as_view(),
        name="manufacturer-list",
    ),
    path(
        "manufacturers/<int:pk>/",
        ManufacturerDetailView.as_view(),
        name="manufacturer-detail",
    ),

    path(
        "cars/",
        CarListView.as_view(),
        name="car-list",
    ),
    path(
        "cars/<int:pk>/",
        CarDetailView.as_view(),
        name="car-detail",
    ),
    path(
        "cars/create/",
        CarCreateView.as_view(),
        name="car-create",
    ),
    path(
        "cars/<int:pk>/update/",
        CarUpdateView.as_view(),
        name="car-update",
    ),
    path(
        "cars/<int:pk>/delete/",
        CarDeleteView.as_view(),
        name="car-delete",
    ),
    path(
        "cars/<int:pk>/assign/",
        assign_me_to_car,
        name="assign-me",
    ),
    path(
        "cars/<int:pk>/delete-assignment/",
        delete_me_from_car,
        name="delete-me",
    ),

    path(
        "drivers/",
        DriverListView.as_view(),
        name="driver-list",
    ),
    path(
        "drivers/<int:pk>/",
        DriverDetailView.as_view(),
        name="driver-detail",
    ),
    path(
        "drivers/create/",
        DriverCreateView.as_view(),
        name="driver-create",
    ),
    path(
        "drivers/<int:pk>/update/",
        DriverLicenseUpdateView.as_view(),
        name="driver-update",
    ),
    path(
        "drivers/<int:pk>/delete/",
        DriverDeleteView.as_view(),
        name="driver-delete",
    ),
]
