from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_LIST_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_create(self):
        res = self.client.get(reverse("taxi:car-create"))
        self.assertNotEqual(res.status_code, 200)

    def test_delete_login_required(self):
        car = Car.objects.create(
            model="Test Model",
            manufacturer=Manufacturer.objects.create(
                name="Test Manufacturer",
                country="Test Country"
            )
        )
        res = self.client.get(
            reverse("taxi:car-delete", args=[car.id])
        )
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.force_login(self.user)

    def test_retrieve_car_list(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_create_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="driver123",
            first_name="Driver",
            last_name="One",
            license_number="UNI12345"
        )
        driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="driver123",
            first_name="Driver",
            last_name="Two",
            license_number="UNI67890"
        )

        form_data = {
            "model": "Test Model",
            "manufacturer": manufacturer.id,
            "drivers": [driver1.id, driver2.id]
        }
        response = self.client.post(reverse("taxi:car-create"), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Car.objects.filter(model="Test Model").exists())

    def test_delete_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country"
        )
        car = Car.objects.create(model="Test Model", manufacturer=manufacturer)
        response = self.client.post(reverse("taxi:car-delete", args=[car.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Car.objects.filter(id=car.id).exists())
