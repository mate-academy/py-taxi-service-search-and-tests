from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicManufacturerTest(TestCase):
    def test_list_manufacturers(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(res.status_code, 200)


class PublicDriverTest(TestCase):
    def test_list_drivers(self):
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_driver_detail(self):
        res = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": 1})
        )
        self.assertNotEqual(res.status_code, 200)


class PublicCarTest(TestCase):
    def test_list_cars(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_car_detail(self):
        res = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": 1})
        )
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="Toyota", country="Japan")

    def test_retrieve_manufacturers(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(
            response, "taxi/manufacturer_list.html"
        )


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="123456789",
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_detail(self):
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="123456789",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Car.objects.create(
            model="testmodel",
            manufacturer=Manufacturer.objects.get(name="Toyota")
        )

    def test_retrieve_cars(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_detail(self):
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")
