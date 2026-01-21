from django.urls import reverse

DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", kwargs={"pk": 1})
DRIVER_CREATE_URL = reverse("taxi:driver-create")
DRIVER_UPDATE_URL = reverse("taxi:driver-update", kwargs={"pk": 1})
DRIVER_DELETE_URL = reverse("taxi:driver-delete", kwargs={"pk": 1})

DRIVERS_URLS = {
    "test_driver_list_url": DRIVER_LIST_URL,
    "test_driver_detail_url": DRIVER_DETAIL_URL,
    "test_driver_create_url": DRIVER_CREATE_URL,
    "test_driver_update_url": DRIVER_UPDATE_URL,
    "test_driver_delete_url": DRIVER_DELETE_URL,
}

DRIVERS_TEMPLATES_PATH = {
    DRIVER_LIST_URL: "taxi/driver_list.html",
    DRIVER_DETAIL_URL: "taxi/driver_detail.html",
    DRIVER_CREATE_URL: "taxi/driver_form.html",
    DRIVER_UPDATE_URL: "taxi/driver_form.html",
    DRIVER_DELETE_URL: "taxi/driver_confirm_delete.html",
}

DRIVERS_DATA = {
    "username": "test",
    "license_number": "ABC12345",
    "password1": "Test1234q",
    "password2": "Test1234q"
}

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
MANUFACTURER_UPDATE_URL = reverse("taxi:manufacturer-update", kwargs={"pk": 1})
MANUFACTURER_DELETE_URL = reverse("taxi:manufacturer-delete", kwargs={"pk": 1})

MANUFACTURER_URLS = {
    "test_manufacturer_list_url": MANUFACTURER_LIST_URL,
    "test_manufacturer_create_url": MANUFACTURER_CREATE_URL,
    "test_manufacturer_update_url": MANUFACTURER_UPDATE_URL,
    "test_manufacturer_delete_url": MANUFACTURER_DELETE_URL,
}

MANUFACTURER_TEMPLATES_PATH = {
    MANUFACTURER_LIST_URL: "taxi/manufacturer_list.html",
    MANUFACTURER_CREATE_URL: "taxi/manufacturer_form.html",
    MANUFACTURER_UPDATE_URL: "taxi/manufacturer_form.html",
    MANUFACTURER_DELETE_URL: "taxi/manufacturer_confirm_delete.html",
}

MANUFACTURER_DATA = {
    "name": "test_name1",
    "country": "test_country_1",
}

CAR_LIST_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = reverse("taxi:car-detail", kwargs={"pk": 1})
CAR_CREATE_URL = reverse("taxi:car-create")
CAR_UPDATE_URL = reverse("taxi:car-update", kwargs={"pk": 1})
CAR_DELETE_URL = reverse("taxi:car-delete", kwargs={"pk": 1})

CAR_URLS = {
    "test_car_list_url": CAR_LIST_URL,
    "test_car_detail_url": CAR_DETAIL_URL,
    "test_car_create_url": CAR_CREATE_URL,
    "test_car_update_url": CAR_UPDATE_URL,
    "test_car_delete_url": CAR_DELETE_URL,
}

CAR_TEMPLATES_PATH = {
    CAR_LIST_URL: "taxi/car_list.html",
    CAR_DETAIL_URL: "taxi/car_detail.html",
    CAR_CREATE_URL: "taxi/car_form.html",
    CAR_UPDATE_URL: "taxi/car_form.html",
    CAR_DELETE_URL: "taxi/car_confirm_delete.html",
}

CAR_DATA = {"model": "test"}

TOGGLE_URL = reverse("taxi:toggle-car-assign", kwargs={"pk": 1})
