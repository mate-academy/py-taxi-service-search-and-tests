from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car, Driver

User = get_user_model()


class SearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser",
                                             password="12345")

        self.manufacturer1 = Manufacturer.objects.create(name="Toyota",
                                                         country="Japan")
        self.manufacturer2 = Manufacturer.objects.create(name="Ford",
                                                         country="USA")

        self.car1 = Car.objects.create(model="Corolla",
                                       manufacturer=self.manufacturer1)
        self.car2 = Car.objects.create(model="Mustang",
                                       manufacturer=self.manufacturer2)

        self.driver1 = Driver.objects.create_user(
            username="driver1", password="driverpass1", license_number="ABC123"
        )
        self.driver2 = Driver.objects.create_user(
            username="driver2", password="driverpass2", license_number="XYZ789"
        )

        self.car1.drivers.add(self.driver1)
        self.car2.drivers.add(self.driver2)

        self.client.login(username="testuser", password="12345")

    def test_manufacturer_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=Toyota"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Toyota")

        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=NonExistent"
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Toyota")

    def test_car_search(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=Corolla")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Mustang")

        response = self.client.get(
            reverse("taxi:car-list") + "?model=NonExistentModel"
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Corolla")
        self.assertNotContains(response, "Mustang")

    def test_driver_search(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=driver1"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver1")
        self.assertNotContains(response, "driver2")

        response = self.client.get(
            reverse("taxi:driver-list") + "?username=NonExistentUser"
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "driver1")
        self.assertNotContains(response, "driver2")
