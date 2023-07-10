from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
CARS_URL = reverse("taxi:car-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="driver1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="test_name1", country="test_country1")
        Manufacturer.objects.create(name="test_name2", country="test_country2")

        response = self.client.get(MANUFACTURERS_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_list_search(self):
        Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        response = self.client.get(MANUFACTURERS_URL, {"name": "test_name"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name="test_name"))
        )


class PublicCarTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CARS_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="driver1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        car1 = Car.objects.create(
            model="test_model_1",
            manufacturer=manufacturer
        )
        car2 = Car.objects.create(
            model="test_model_2",
            manufacturer=manufacturer
        )
        car1.drivers.add(self.user, )
        car2.drivers.add(self.user, )

        response = self.client.get(CARS_URL)

        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_list_search(self):
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        Car.objects.create(model="test_model", manufacturer=manufacturer)
        response = self.client.get(CARS_URL, {"model": "test_model"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model="test_model"))
        )


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="driver1234",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "test_username",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "TES12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
