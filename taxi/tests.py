from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverLicenseUpdateForm
from taxi.models import Car, Driver, Manufacturer


class TaxiTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="tester", password="password", license_number="QQQ11111"
        )
        self.client.force_login(self.user)

    def test_license_number_validation(self):
        valid = DriverLicenseUpdateForm(data={"license_number": "QQQ12345"})
        self.assertTrue(valid.is_valid())

    def test_toggle_assign_to_car(self):
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        car = Car.objects.create(model="Focus", manufacturer=manufacturer)
        url = reverse("taxi:toggle-car-assign", args=[car.pk])

        self.client.post(url)
        self.assertIn(self.user, car.drivers.all())

        self.client.post(url)
        self.assertNotIn(self.user, car.drivers.all())

    def test_driver_search_by_username(self):
        alice = Driver.objects.create_user(
            username="alice", password="password", license_number="QQQ22222"
        )
        Driver.objects.create_user(
            username="bob", password="password", license_number="WWW11111"
        )

        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "ALI"}
        )

        self.assertEqual(list(response.context["driver_list"]), [alice])

    def test_car_search_by_model(self):
        manufacturer = Manufacturer.objects.create(name="Ford", country="USA")
        mustang = Car.objects.create(
            model="Mustang", manufacturer=manufacturer
        )
        Car.objects.create(model="Focus", manufacturer=manufacturer)

        response = self.client.get(reverse("taxi:car-list"), {"model": "must"})

        self.assertEqual(list(response.context["car_list"]), [mustang])

    def test_manufacturer_search_by_name(self):
        toyota = Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="BMW", country="Germany")

        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "toy"}
        )

        self.assertEqual(
            list(response.context["manufacturer_list"]), [toyota]
        )
