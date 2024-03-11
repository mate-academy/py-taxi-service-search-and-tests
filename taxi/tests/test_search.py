from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


class TestSearch(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="Test123"
        )
        self.client.force_login(self.user)

        Driver.objects.create(
            username="test1",
            password="12345",
            license_number="AAA00000"
        )
        Driver.objects.create(
            username="test2",
            password="12345",
            license_number="AAA00001"
        )
        Driver.objects.create(
            username="exdriver",
            password="12345",
            license_number="AAA00002"
        )

        Manufacturer.objects.create(
            name="test1",
            country="Any"
        )
        Manufacturer.objects.create(
            name="man1",
            country="Any"
        )

        Car.objects.create(
            model="test1",
            manufacturer=Manufacturer.objects.get(id=1)
        )
        Car.objects.create(
            model="excar",
            manufacturer=Manufacturer.objects.get(id=2)
        )

    def test_search_drivers_check_values(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "test"}
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "test1")
        self.assertContains(response, "test2")
        self.assertNotContains(response, "exdriver")

    def test_search_manufacturer_check_values(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "test1"}
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "test1")
        self.assertNotContains(response, "man1")

    def test_search_car_check_values(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "test1"}
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "test1")
        self.assertNotContains(response, "excar")
