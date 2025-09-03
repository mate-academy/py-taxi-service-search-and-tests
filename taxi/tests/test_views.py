from http.client import responses

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from urllib.parse import urlencode

from taxi.models import Manufacturer, Car

CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")

car_base_url = reverse("taxi:car-list")
car_params = urlencode({"model": "M4"})
CAR_FILTER_URL = f"{car_base_url}?{car_params}"

driver_base_url = reverse("taxi:driver-list")
driver_params = urlencode({"username": "test"})
DRIVER_FILTER_URL = f"{driver_base_url}?{driver_params}"

manufacturer_base_url = reverse("taxi:manufacturer-list")
manufacturer_params = urlencode({"name": "BMW"})
MANUFACTURER_FILTER_URL = f"{manufacturer_base_url}?{manufacturer_params}"


class PublicViewsTests(TestCase):

    def test_login_required(self):
        car_list = self.client.get(CAR_LIST_URL)
        driver_list = self.client.get(DRIVER_LIST_URL)
        manufacturer_list = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEqual(car_list.status_code, 200)
        self.assertNotEqual(driver_list.status_code, 200)
        self.assertNotEqual(manufacturer_list.status_code, 200)


class PrivateViewsTests(TestCase):

    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="TES12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="test country"
        )
        self.car = Car.objects.create(
            model="M4",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)
        self.client.force_login(self.driver)

    def test_login_required(self):
        car_list = self.client.get(CAR_LIST_URL)
        driver_list = self.client.get(DRIVER_LIST_URL)
        manufacturer_list = self.client.get(MANUFACTURER_LIST_URL)

        self.assertEqual(car_list.status_code, 200)
        self.assertEqual(driver_list.status_code, 200)
        self.assertEqual(manufacturer_list.status_code, 200)

    def test_forms_initial(self):
        response = self.client.get(CAR_FILTER_URL)
        search_form = response.context["search_form"]
        self.assertEqual(search_form.initial.get("model"), self.car.model)

        response = self.client.get(DRIVER_FILTER_URL)
        search_form = response.context["search_form"]
        self.assertEqual(search_form.initial.get("username"),
                         self.driver.username)

        response = self.client.get(MANUFACTURER_FILTER_URL)
        search_form = response.context["search_form"]
        self.assertEqual(
            search_form.initial.get("name"),
            self.manufacturer.name
        )

    def test_queryset_filters(self):
        response = self.client.get(CAR_FILTER_URL)
        queryset = response.context["object_list"]
        self.assertEqual(
            list(queryset),
            list(Car.objects.filter(model__icontains=self.car.model))
        )

        response = self.client.get(DRIVER_FILTER_URL)
        queryset = response.context["object_list"]
        self.assertEqual(
            list(queryset),
            list(get_user_model().objects.filter(
                username__icontains=self.driver.username))
        )

        response = self.client.get(MANUFACTURER_FILTER_URL)
        queryset = response.context["object_list"]
        self.assertEqual(
            list(queryset),
            list(Manufacturer.objects.filter(
                name__icontains=self.manufacturer.name))
        )
