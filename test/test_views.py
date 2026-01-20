from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car, Driver


class TaxiAppTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )
        self.driver = Driver.objects.create(
            username="driver1",
            password="testpass",
            license_number="AB12345"
        )

    def test_manufacturer_list_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertContains(response, self.manufacturer.name)

    def test_car_list_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertContains(response, self.car.model)

    def test_driver_list_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertContains(response, self.driver.username)

    def test_car_detail_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(
            reverse("taxi:car-detail",
                    kwargs={"pk": self.car.id}
                    )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")
        self.assertContains(response, self.car.model)

    def test_manufacturer_create_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            {"name": "Honda", "country": "Japan"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="Honda").exists())

    def test_car_create_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("taxi:car-create"), {
            "model": "Accord",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id],
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Car.objects.filter(model="Accord").exists())

    def test_driver_create_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("taxi:driver-create"), {
            "username": "driver2",
            "password1": "newpass123",
            "password2": "newpass123",
            "license_number": "XYZ78901"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Driver.objects.filter(username="driver2").exists())
