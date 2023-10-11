from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEquals(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test1234"
        )

        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "test_username",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "password1": "test1234",
            "password2": "test1234",
            "license_number": "TEST_LICENSE"
        }
        response = self.client.post(
            reverse("taxi:driver-create"),
            data=form_data
        )
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEquals(
            new_driver.username,
            form_data["username"]
        )
        self.assertEquals(
            new_driver.last_name,
            form_data["last_name"]
        )
        self.assertEquals(
            new_driver.license_number,
            form_data["license_number"]
        )


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test1234"
        )

        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="country1"
        )
        Car.objects.create(model="Opel", manufacturer=manufacturer)
        Car.objects.create(model="Nissan", manufacturer=manufacturer)
        response = self.client.get(CAR_URL)
        self.assertEquals(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEquals(
            list(response.context["car_list"]),
            list(cars)
        )
