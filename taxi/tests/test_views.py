from django.contrib.auth import get_user_model
from django.contrib.sites import requests
from django.test import TestCase, RequestFactory
from django.urls import reverse

from taxi.forms import (
    DriverListSearchForm,
    CarListSearchForm,
    ManufacturerListSearchForm,
)
from taxi.models import Manufacturer, Car
from taxi.views import DriverListView, CarListView, ManufacturerListView

DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicAccessTest(TestCase):

    def test_login_driver_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_car_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_manufacturer_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateAccessTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user_1 = get_user_model().objects.create_user(
            username="testuser", password="test123", license_number="ABC12345"
        )
        self.user_2 = get_user_model().objects.create_user(
            username="testuser2", password="test321", license_number="ADB32145"
        )
        self.client.force_login(self.user_1)

        self.manufacturer_2 = Manufacturer.objects.create(name="Dodge",
                                                          country="USA")
        self.manufacturer_1 = Manufacturer.objects.create(name="Zaz",
                                                          country="Ukraine")

        self.car_1 = Car.objects.create(
            model="Sens",
            manufacturer=self.manufacturer_1,
        )
        self.car_1.drivers.set([self.user_1])

        self.car_2 = Car.objects.create(model="Viper",
                                        manufacturer=self.manufacturer_2)
        self.car_2.drivers.set([self.user_2])

    def common_test_context_data_and_queryset(
        self,
        url,
        view_class,
        form_class,
        search_param,
        search_value,
        expected_values,
        field_name,
    ):
        request = self.factory.get(url, {search_param: search_value})
        request.user = self.user_1

        view = view_class.as_view()
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context_data)
        self.assertIsInstance(response.context_data["search_form"], form_class)
        self.assertEqual(
            response.context_data["search_form"].initial[search_param],
            search_value
        )

        actual_values = list(
            response.context_data["object_list"].values_list(field_name,
                                                             flat=True)
        )
        self.assertEqual(actual_values, expected_values)

    def test_car_context_data_and_queryset(self):
        self.common_test_context_data_and_queryset(
            url=CAR_URL,
            view_class=CarListView,
            form_class=CarListSearchForm,
            search_param="model",
            search_value="Sens",
            expected_values=["Sens"],
            field_name="model",
        )

    def test_driver_context_data_and_queryset(self):
        self.common_test_context_data_and_queryset(
            url=DRIVER_URL,
            view_class=DriverListView,
            form_class=DriverListSearchForm,
            search_param="username",
            search_value="testuser2",
            expected_values=["testuser2"],
            field_name="username",
        )

    def test_manufacturer_context_data_and_queryset(self):
        self.common_test_context_data_and_queryset(
            url=MANUFACTURER_URL,
            view_class=ManufacturerListView,
            form_class=ManufacturerListSearchForm,
            search_param="name",
            search_value="Dodge",
            expected_values=["Dodge"],
            field_name="name",
        )

    def test_assign_to_car(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car_2.id])

        self.assertNotIn(self.car_2, self.user_1.cars.all())

        response = self.client.post(url)
        self.assertRedirects(response, reverse("taxi:car-detail",
                                               args=[self.car_2.id]))

        self.user_1.refresh_from_db()
        self.assertIn(self.car_2, self.user_1.cars.all())

    def test_unassigned_to_car(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car_2.id])

        self.user_1.cars.add(self.car_2)
        self.assertIn(self.car_2, self.user_1.cars.all())

        response = self.client.post(url)
        self.assertRedirects(response, reverse("taxi:car-detail",
                                               args=[self.car_2.id]))

        self.user_1.refresh_from_db()
        self.assertNotIn(self.car_2, self.user_1.cars.all())
