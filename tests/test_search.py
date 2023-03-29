from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")


class SearchFeatureTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123"
        )
        self.client.force_login(self.user)

        self.driver1 = get_user_model().objects.create_user(
            username="test1",
            password="1234test123",
            first_name="Pimp1",
            last_name="Lazo1",
            license_number="ABC12345"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="test2",
            password="1234test123",
            first_name="Pimp2",
            last_name="Lazo2",
            license_number="ABC12346"
        )
        self.driver3 = get_user_model().objects.create_user(
            username="Giovanni",
            password="1234test123",
            first_name="Joe",
            last_name="Bobotto",
            license_number="ABC12347"
        )
        self.manufacturer1 = Manufacturer.objects.create(
            name="Test1",
            country="Test1"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Test2",
            country="Test2"
        )
        self.car1 = Car.objects.create(
            model="TestModel1",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="TestModel2",
            manufacturer=self.manufacturer2
        )

    def test_empty_search_form(self):
        res = self.client.get(MANUFACTURER_LIST_URL, {"title": ""})

        self.assertContains(res, self.manufacturer1.country)
        self.assertContains(res, self.manufacturer2.name)

    def test_success_search_with_partly_match(self):
        res = self.client.get(DRIVER_LIST_URL, {"title": "est"})

        self.assertContains(res, self.driver1.first_name)
        self.assertContains(res, self.driver2.last_name)
        self.assertNotContains(res, self.driver3)

    def test_search_with_absent_car(self):
        res = self.client.get(CAR_LIST_URL, {"title": "Tesla"})

        self.assertNotContains(res, self.car1)
        self.assertNotContains(res, self.car2)
