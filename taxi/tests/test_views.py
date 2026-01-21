from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer

DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)
        get_user_model().objects.create_user(
            username="test_user2",
            password="<5555555>",
            license_number="USE55555",
        )
        get_user_model().objects.create_user(
            username="test_driver",
            password="123123",
            license_number="TTT789")

    def test_retrieve_driver_list(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)

        drivers = Driver.objects.all()
        self.assertEqual(list(response.context["driver_list"]),
                         list(drivers))

        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_search_by_username(self):
        drivers = Driver.objects.filter(username__icontains="test_user")
        response = self.client.get(DRIVER_LIST_URL + "?username=test_user")
        self.assertEqual(list(response.context["driver_list"]),
                         list(drivers))

    def test_create_driver(self):
        form_data = {
            "username": "new_user3",
            "license_number": "TOT11111",
            "password1": "<PASSWORD12",
            "password2": "<PASSWORD12",
            "first_name": "Test",
            "last_name": "User",

        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"])
        self.assertEqual(new_driver.first_name,
                         form_data["first_name"])
        self.assertEqual(new_driver.last_name,
                         form_data["last_name"])
        self.assertEqual(new_driver.license_number,
                         form_data["license_number"])


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)
        Manufacturer.objects.create(name="test_manufacturer", country="UK")
        Manufacturer.objects.create(name="test_manufacturer2", country="US")

    def test_manufacturer_create(self):
        form_data = {
            "name": "new_manufacturer",
            "country": "Germany",
        }
        self.client.post(reverse("taxi:manufacturer-create"), data=form_data)
        new_manufacturer = Manufacturer.objects.get(name=form_data["name"])
        self.assertEqual(new_manufacturer.name, form_data["name"])

    def test_manufacturer_search_by_name(self):
        manufacturers = Manufacturer.objects.filter(
            name__icontains="test_manufacturer")
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=test_manufacturer")
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturers))
