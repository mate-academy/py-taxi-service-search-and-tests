from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car, Driver


class TestForm(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tset",
            password="test12345",
        )

        self.client.force_login(self.user)

    def test_car_should_search_by_name(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )

        Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )
        cars = Car.objects.all()
        response = self.client.get(reverse("taxi:car-list") + "?model=test")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertEqual(list(response.context["car_list"]), list(cars))

    def test_driver_should_search_by_username(self):
        Driver.objects.create(
            username="test", password="test12345", license_number="ABC12345"
        )
        drivers = Driver.objects.all()

        response = self.client.get(
            reverse("taxi:driver-list") + "?username=test"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertEqual(list(response.context["driver_list"]), list(drivers))

    def test_manufacturer_should_search_by_name(self):
        Manufacturer.objects.create(
            name="test",
            country="test_country"
        )
        manufacturers = Manufacturer.objects.all()
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=test"
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
