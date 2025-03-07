from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicCarTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )
        self.car_list_url = reverse("taxi:car-list")
        self.car_detail_url = reverse(
            "taxi:car-detail",
            kwargs={"pk": self.car.pk}
        )

    def test_login_required(self):
        res = self.client.get(self.car_list_url)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_detail(self):
        res = self.client.get(self.car_detail_url)
        self.assertNotEqual(res.status_code, 200)


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="test", country="country_test")
        Manufacturer.objects.create(name="test2", country="country_test2")
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="username",
            password="password",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test First",
            "last_name": "Test Last",
            "license_number": "ABC12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )
        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"]
        )
