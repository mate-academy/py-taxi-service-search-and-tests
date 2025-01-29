from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer


Driver = get_user_model()


class ToggleAssignToCarTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = Driver.objects.create_user(
            username="testdriver",
            password="password123",
            license_number="AAB12355"
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="test m",
            country="Test country"
        )
        cls.car = Car.objects.create(
            model="Test Car",
            manufacturer=cls.manufacturer
        )

    def test_toggle_assign_to_car(self):
        self.client.login(username="testdriver", password="password123")

        self.assertFalse(self.driver.cars.filter(pk=self.car.pk).exists())

        response = self.client.post(
            reverse(
                "taxi:toggle-car-assign",
                args=[self.car.pk])
        )
        self.assertRedirects(
            response,
            reverse("taxi:car-detail", args=[self.car.pk])
        )
        self.assertTrue(self.driver.cars.filter(pk=self.car.pk).exists())

        response = self.client.post(
            reverse(
                "taxi:toggle-car-assign",
                args=[self.car.pk])
        )
        self.assertRedirects(
            response,
            reverse("taxi:car-detail", args=[self.car.pk])
        )
        self.assertFalse(self.driver.cars.filter(pk=self.car.pk).exists())


class ManufacturerListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            password="passreyerdy23"
        )
        cls.manufacturer1 = Manufacturer.objects.create(
            name="Has Test",
            country="china"
        )
        cls.manufacturer2 = Manufacturer.objects.create(
            name="Test as well",
            country="usa"
        )
        cls.manufacturer3 = Manufacturer.objects.create(
            name="Not",
            country="uganda"
        )

    def test_search_no_match(self):
        self.client.login(
            username="testuser",
            password="passreyerdy23"
        )
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "NO MATCH"}
        )
        self.assertNotContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer2.name)
        self.assertNotContains(response, self.manufacturer3.name)

    def test_search_match_all(self):
        self.client.login(
            username="testuser",
            password="passreyerdy23"
        )
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "t"}
        )
        self.assertContains(response, self.manufacturer1.name)
        self.assertContains(response, self.manufacturer2.name)
        self.assertContains(response, self.manufacturer3.name)

    def test_search_match_two(self):
        self.client.login(
            username="testuser",
            password="passreyerdy23"
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Test"}
        )
        self.assertContains(response, self.manufacturer1.name)
        self.assertContains(response, self.manufacturer2.name)
        self.assertNotContains(response, self.manufacturer3.name)
