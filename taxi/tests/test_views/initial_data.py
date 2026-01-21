from django.urls import reverse

DRIVERS_URLS = {
    "test_driver_list_url": reverse("taxi:driver-list"),
    "test_driver_detail_url": reverse(
        "taxi:driver-detail", kwargs={"pk": 1}
    ),
    "test_driver_create_url": reverse("taxi:driver-create"),
    "test_driver_update_url": reverse(
        "taxi:driver-update", kwargs={"pk": 1}
    ),
    "test_driver_delete_url": reverse(
        "taxi:driver-delete", kwargs={"pk": 1}
    ),
}

DRIVERS_TEMPLATES_PATH = {
    reverse("taxi:driver-list"): "taxi/driver_list.html",
    reverse(
        "taxi:driver-detail", kwargs={"pk": 1}
    ): "taxi/driver_detail.html",
    reverse("taxi:driver-create"): "taxi/driver_form.html",
    reverse(
        "taxi:driver-update", kwargs={"pk": 1}
    ): "taxi/driver_form.html",
    reverse(
        "taxi:driver-delete", kwargs={"pk": 1}
    ): "taxi/driver_confirm_delete.html",
}

DRIVERS_DATA = {
    "username": "test",
    "license_number": "ABC12345",
    "password1": "Test1234q",
    "password2": "Test1234q"
}

MANUFACTURER_URLS = {
    "test_manufacturer_list_url": reverse("taxi:manufacturer-list"),
    "test_manufacturer_create_url": reverse("taxi:manufacturer-create"),
    "test_manufacturer_update_url": reverse(
        "taxi:manufacturer-update", kwargs={"pk": 1}
    ),
    "test_manufacturer_delete_url": reverse(
        "taxi:manufacturer-delete", kwargs={"pk": 1}
    ),
}

MANUFACTURER_TEMPLATES_PATH = {
    reverse("taxi:manufacturer-list"): "taxi/manufacturer_list.html",
    reverse("taxi:manufacturer-create"): "taxi/manufacturer_form.html",
    reverse(
        "taxi:manufacturer-update", kwargs={"pk": 1}
    ): "taxi/manufacturer_form.html",
    reverse(
        "taxi:manufacturer-delete", kwargs={"pk": 1}
    ): "taxi/manufacturer_confirm_delete.html",
}

MANUFACTURER_DATA = {
    "name": "test_name1",
    "country": "test_country_1",
}

CAR_URLS = {
    "test_car_list_url": reverse("taxi:car-list"),
    "test_car_detail_url": reverse("taxi:car-detail", kwargs={"pk": 1}),
    "test_car_create_url": reverse("taxi:car-create"),
    "test_car_update_url": reverse("taxi:car-update", kwargs={"pk": 1}),
    "test_car_delete_url": reverse("taxi:car-delete", kwargs={"pk": 1}),
}

CAR_TEMPLATES_PATH = {
    reverse("taxi:car-list"): "taxi/car_list.html",
    reverse(
        "taxi:car-detail", kwargs={"pk": 1}
    ): "taxi/car_detail.html",
    reverse("taxi:car-create"): "taxi/car_form.html",
    reverse("taxi:car-update", kwargs={"pk": 1}): "taxi/car_form.html",
    reverse(
        "taxi:car-delete", kwargs={"pk": 1}
    ): "taxi/car_confirm_delete.html",
}

CAR_DATA = {"model": "test"}

TOGGLE_URL = reverse("taxi:toggle-car-assign", kwargs={"pk": 1})
