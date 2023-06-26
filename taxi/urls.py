from django.urls import path

from .views import (
    index,
    CarListView,
    CarDetailView,
    CarCreateView,
    CarUpdateView,
    CarDeleteView,
    DriverListView,
    DriverDetailView,
    DriverCreateView,
    DriverLicenseUpdateView,
    DriverDeleteView,
    ManufacturerListView,
    ManufacturerDetailView,
    ManufacturerCreateView,
    ManufacturerUpdateView,
    ManufacturerDeleteView,
    toggle_assign_to_car,
    RegistrationView,
    CommentDeleteView,
    DriverSettingsView,
    registration_complete,
    like_and_unlike,
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "manufacturers/",
        ManufacturerListView.as_view(),
        name="manufacturer-list",
    ),
    path(
        "manufacturers/create/",
        ManufacturerCreateView.as_view(),
        name="manufacturer-create",
    ),
    path(
        "manufacturers/<int:pk>/update/",
        ManufacturerUpdateView.as_view(),
        name="manufacturer-update",
    ),
    path(
        "manufacturers/<int:pk>/delete/",
        ManufacturerDeleteView.as_view(),
        name="manufacturer-delete",
    ),
    path(
        "manufacturers/<int:pk>/",
        ManufacturerDetailView.as_view(),
        name="manufacturer-detail",
    ),
    path(
        "cars/<int:id>/comment/<int:pk>/delete",
        CommentDeleteView.as_view(),
        name="delete_comment",
    ),
    path("cars/", CarListView.as_view(), name="car-list"),
    path("cars/<int:pk>/", CarDetailView.as_view(), name="car-detail"),
    path("cars/create/", CarCreateView.as_view(), name="car-create"),
    path("cars/<int:pk>/update/", CarUpdateView.as_view(), name="car-update"),
    path("cars/<int:pk>/delete/", CarDeleteView.as_view(), name="car-delete"),
    path(
        "cars/<int:pk>/toggle-assign/",
        toggle_assign_to_car,
        name="toggle-car-assign",
    ),
    path("drivers/", DriverListView.as_view(), name="driver-list"),
    path(
        "drivers/<int:pk>/", DriverDetailView.as_view(), name="driver-detail"
    ),
    path("drivers/", DriverListView.as_view(), name="driver-list"),
    path(
        "drivers/<int:pk>/", DriverDetailView.as_view(), name="driver-detail"
    ),
    path(
        "drivers/<int:pk>/settings/",
        DriverSettingsView.as_view(),
        name="driver-settings",
    ),
    path("drivers/create/", DriverCreateView.as_view(), name="driver-create"),
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
    path(
        "login/registration/",
        RegistrationView.as_view(),
        name="driver-registration",
    ),
    path(
        "login/registration/complete/",
        registration_complete,
        name="registration-complete",
    ),
    path(
        "cars/<int:id>/comment/<int:pk>/like",
        like_and_unlike,
        name="like_comment",
    ),
]

app_name = "taxi"
