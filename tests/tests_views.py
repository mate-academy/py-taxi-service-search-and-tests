from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Manufacturer


class TestViewsIsPrivate(TestCase):
    def test_car_list_is_private(self):
        url = "http://localhost/cars/"
        response = self.client.get(url)
        self.assertNotEquals(response.status_code, 200)

    def test_driver_list_is_private(self):
        url = "http://localhost/drivers/"
        response = self.client.get(url)
        self.assertNotEquals(response.status_code, 200)

    def test_manufacturer_list_is_private(self):
        url = "http://localhost/manufacturers/"
        response = self.client.get(url)
        self.assertNotEquals(response.status_code, 200)


class TestViewsUnlocked(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test", password="test-123"
        )
        self.client.force_login(self.user)

    def test_car_list_is_unlocked(self):
        Car.objects.create(
            model="test2",
            manufacturer=Manufacturer.objects.create(
                name="test2",
                country="test"
            ),
        )
        Car.objects.create(
            model="test1",
            manufacturer=Manufacturer.objects.create(
                name="test1",
                country="test"
            ),
        )
        url = "http://localhost/cars/"
        response = self.client.get(url)
        cars = Car.objects.all()
        self.assertEquals(response.status_code, 200)
        self.assertEquals(list(cars), list(response.context["car_list"]))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_driver_list_is_unlocked(self):
        url = "http://localhost/drivers/"
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_manufacturer_list_is_unlocked(self):
        url = "http://localhost/manufacturers/"
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
