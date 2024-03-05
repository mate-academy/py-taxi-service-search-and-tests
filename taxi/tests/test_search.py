from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


class TestSearch(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="Test123"
        )
        self.client.force_login(self.user)

        Driver.objects.create(
            username="Atest",
            password="123qwery",
            license_number="ADC12345"
        )
        Driver.objects.create(
            username="atest",
            password="123qwery",
            license_number="ABC12534"
        )
        Driver.objects.create(
            username="btest",
            password="123qwery",
            license_number="ABC51234"
        )
        Manufacturer.objects.create(
            name="Atest",
            country="Anywhere"
        )
        Manufacturer.objects.create(
            name="atest",
            country="Anywhere"
        )
        Manufacturer.objects.create(
            name="btest",
            country="Anywhere"
        )
        Car.objects.create(
            model="Atest",
            manufacturer=Manufacturer.objects.get(id=1)
        )
        Car.objects.create(
            model="atest",
            manufacturer=Manufacturer.objects.get(id=1)
        )
        Car.objects.create(
            model="btest",
            manufacturer=Manufacturer.objects.get(id=1)
        )

    def test_search_drivers_check_values(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "a"}
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Atest")
        self.assertContains(response, "atest")
        self.assertNotContains(response, "btest")

    def test_search_drivers_check_len(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "a"}
        )
        self.assertEqual(
            len(response.context_data["object_list"]),
            len(Driver.objects.filter(username__icontains="A"))
        )

    def test_search_cars_check_values(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "a"}
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Atest")
        self.assertContains(response, "atest")
        self.assertNotContains(response, "btest")

    def test_search_car_check_len(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "a"}
        )
        self.assertEqual(
            len(response.context_data["object_list"]),
            len(Car.objects.filter(model__icontains="A"))
        )

    def test_search_manufacturer_check_values(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "a"}
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Atest")
        self.assertContains(response, "atest")
        self.assertNotContains(response, "btest")

    def test_search_manufacturer_check_len(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "a"}
        )
        self.assertEqual(
            len(response.context_data["object_list"]),
            len(Manufacturer.objects.filter(name__icontains="A"))
        )
