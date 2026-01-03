from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


DRIVER_LIST_URL = reverse("taxi:driver-list")

class DriversSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="semde",
            password="test_password"
        )
        self.client.force_login(self.user)

        self.driver1 = Driver.objects.create(
            username="john",
            license_number="AAA1111",
            first_name="John",
            last_name="Smith",
        )
        self.driver2 = Driver.objects.create(
            username="jane",
            license_number="AAA2222",
            first_name="Jane",
            last_name="Smith",
        )
        self.driver3 = Driver.objects.create(
            username="kent",
            license_number="AAA3333",
            first_name="Kent",
            last_name="Smith",
        )
        manufacturer = Manufacturer.objects.create(name="Audi")
        self.car = Car.objects.create(
            model="testmodel",
            manufacturer=manufacturer,)

    def test_drivers_search(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        search_response = self.client.get(DRIVER_LIST_URL, {"username": "jane"})
        self.assertEqual(search_response.status_code, 200)
        drivers = search_response.context["driver_list"]
        self.assertEqual(len(drivers), 1)

    def test_toggle_assign_to_car_driver_add(self):
        self.client.force_login(self.driver1)
        self.assertNotIn(self.driver1, self.car.drivers.all())
        self.car.drivers.add(self.driver1)
        toggle_url = reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.pk})
        response = self.client.get(toggle_url)
        self.assertEqual(response.status_code, 302)

    def test_toggle_assign_to_car_driver_remove(self):
        self.client.force_login(self.driver1)
        self.car.drivers.add(self.driver1)
        self.assertIn(self.driver1, self.car.drivers.all())
        toggle_url = reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.pk})
        response = self.client.get(toggle_url)
        self.assertEqual(response.status_code, 302)
        self.car.refresh_from_db()
        self.assertNotIn(self.driver1, self.car.drivers.all())
