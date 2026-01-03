from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class TestLoginRequired(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="test_user",
            password="Test123",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test_Manufacturer",
            country="Test_Country",
        )
        self.car = Car.objects.create(
            model="Test_Model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_login_required(self):

        urls = [
            reverse("taxi:index"),
            reverse("taxi:manufacturer-list"),
            reverse("taxi:manufacturer-create"),
            reverse("taxi:manufacturer-update", args=(self.manufacturer.id,)),
            reverse("taxi:manufacturer-delete", args=(self.manufacturer.id,)),
            reverse("taxi:car-list"),
            reverse("taxi:car-detail", args=(self.car.id,)),
            reverse("taxi:car-create"),
            reverse("taxi:car-update", args=(self.car.id,)),
            reverse("taxi:car-delete", args=(self.car.id,)),
            reverse("taxi:toggle-car-assign", args=(self.car.id,)),
            reverse("taxi:driver-list"),
            reverse("taxi:driver-detail", args=(self.driver.id,)),
            reverse("taxi:driver-create"),
            reverse("taxi:driver-update", args=(self.driver.id,)),
            reverse("taxi:driver-delete", args=(self.driver.id,)),

        ]
        for url in urls:
            res = self.client.get(url)
            self.assertNotEqual(res.status_code, 200)
