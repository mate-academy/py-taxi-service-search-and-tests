from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class ManufacturerPublicTest(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(response.status_code, 200)


class ManufacturerPrivateTest(TestCase):
    def test_receive_manufacturers(self):
        self.user = get_user_model().objects.create_user(
            username="admin_test",
            password="12345test"
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="Subaru test")
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.all())
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class CarPublicTest(TestCase):
    def test_login_required(self):

        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)


class CarPrivateTest(TestCase):
    def test_receive_cars(self):

        self.user = get_user_model().objects.create_user(
            username="admin_test",
            password="12345test"
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(name="Subaru test")
        Car.objects.create(
            model="Boxer",
            manufacturer=manufacturer
        )
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.all())
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class DriverPublicTest(TestCase):
    def test_login_required(self):

        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)


class DriverPrivateTest(TestCase):
    def test_receive_drivers(self):

        self.user = get_user_model().objects.create_user(
            username="admin_test",
            password="12345test"
        )
        self.client.force_login(self.user)

        Driver.objects.create(
            username="driver_test_name",
            password="password111",
            license_number="KAA33333"
        )
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(Driver.objects.all())
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
