from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Car


class SearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="admin",
            password="password",
            license_number="AAA11111"
        )
        cls.man = Manufacturer.objects.create(name="Toyota")
        Car.objects.create(model="Corolla", manufacturer=cls.man)

        get_user_model().objects.create_user(
            username="driver.test",
            password="password",
            license_number="BBB22222"
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_manufacturer_search(self):
        res = self.client.get(reverse("taxi:manufacturer-list"),
                              {"title": "toy"}
                              )
        self.assertContains(res, "Toyota")

    def test_car_search(self):
        res = self.client.get(reverse("taxi:car-list"), {"title": "cor"})
        self.assertContains(res, "Corolla")

    def test_driver_search(self):
        res = self.client.get(reverse("taxi:driver-list"), {"title": "test"})
        self.assertContains(res, "driver.test")
