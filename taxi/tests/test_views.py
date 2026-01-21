from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car, Driver
from django.test import Client


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345"
        )
        self.client.login(username="testuser", password="testpass123")
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )
        self.driver = Driver.objects.create(
            username="driver1",
            license_number="XYZ67890"
        )

    def test_manufacturer_create_view(self):
        response = self.client.post(
            reverse(
                "taxi:manufacturer-create"
            ),
            {"name": "Honda", "country": "Japan"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="Honda").exists())

    def test_manufacturer_update_view(self):
        response = self.client.post(
            reverse(
                "taxi:manufacturer-update",
                args=[self.manufacturer.pk]
            ),
            {"name": "Subaru", "country": "Japan"})
        self.assertEqual(response.status_code, 302)
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, "Subaru")

    def test_manufacturer_delete_view(self):
        response = self.client.post(
            reverse(
                "taxi:manufacturer-delete",
                args=[self.manufacturer.pk]
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Manufacturer.objects.filter(
            pk=self.manufacturer.pk).exists())

    def test_car_list_view(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertContains(response, "Corolla")

    def test_car_detail_view(self):
        response = self.client.get(
            reverse(
                "taxi:car-detail",
                args=[self.car.pk]
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")
        self.assertContains(response, "Corolla")

    def test_car_create_view(self):
        response = self.client.post(reverse("taxi:car-create"), {
            "model": "Camry",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.driver.pk]
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Car.objects.filter(model="Camry").exists())

    def test_car_update_view(self):
        response = self.client.post(
            reverse(
                "taxi:car-update",
                args=[self.car.pk]
            ), {
                "model": "Camry",
                "manufacturer": self.manufacturer.pk,
                "drivers": [self.driver.pk]
            }
        )
        self.assertEqual(response.status_code, 302)
        self.car.refresh_from_db()
        self.assertEqual(self.car.model, "Camry")

    def test_car_delete_view(self):
        response = self.client.post(
            reverse(
                "taxi:car-delete",
                args=[self.car.pk]
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Car.objects.filter(pk=self.car.pk).exists())

    def test_driver_list_view(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertContains(response, "driver1")

    def test_driver_detail_view(self):
        response = self.client.get(
            reverse(
                "taxi:driver-detail",
                args=[self.driver.pk]
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")
        self.assertContains(response, "driver1")

    def test_driver_create_view(self):
        response = self.client.post(reverse("taxi:driver-create"), {
            "username": "newdriver",
            "password1": "testpass123",
            "password2": "testpass123",
            "license_number": "DEF67890",
            "first_name": "New",
            "last_name": "Driver"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Driver.objects.filter(username="newdriver").exists())
