from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer
from taxi.tests.base import LoggedInTestCase

INDEX_URL = reverse("taxi:index")


class PublicAccessTest(TestCase):
    def test_all_views_require_login(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        car = Car.objects.create(model="Corolla", manufacturer=manufacturer)
        driver = get_user_model().objects.create_user(
            username="driver", password="test12345", license_number="XYZ98765"
        )
        urls = [
            INDEX_URL,
            reverse("taxi:car-list"),
            reverse("taxi:car-create"),
            reverse("taxi:car-detail", args=[car.pk]),
            reverse("taxi:car-update", args=[car.pk]),
            reverse("taxi:car-delete", args=[car.pk]),
            reverse("taxi:driver-list"),
            reverse("taxi:driver-create"),
            reverse("taxi:driver-detail", args=[driver.pk]),
            reverse("taxi:driver-update", args=[driver.pk]),
            reverse("taxi:driver-delete", args=[driver.pk]),
            reverse("taxi:toggle-car-assign", args=[car.pk]),
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(
                    response, f"{settings.LOGIN_URL}?next={url}"
                )


class ToggleAssignToCarTest(LoggedInTestCase):
    def test_toggle_adds_and_removes_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        car = Car.objects.create(model="Corolla", manufacturer=manufacturer)
        url = reverse("taxi:toggle-car-assign", args=[car.pk])

        response = self.client.get(url)
        self.assertRedirects(
            response, reverse("taxi:car-detail", args=[car.pk])
        )
        self.assertIn(car, self.user.cars.all())

        self.client.get(url)
        self.assertNotIn(car, self.user.cars.all())
