from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Driver, Car, Manufacturer

DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicTests(TestCase):

    def test_driver_login_required(self):
        res = self.client.get(DRIVER_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_car_login_required(self):
        res = self.client.get(CAR_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_manufacturer_login_required(self):
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "user123test"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="test1",
            country="test country1"
        )
        Manufacturer.objects.create(
            name="test2",
            country="test country2"
        )

        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "test2",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TES12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_search_field_driver(self):
        Manufacturer.objects.create(
            name="test1",
            country="test country1"
        )
        Manufacturer.objects.create(
            name="test2",
            country="test country2"
        )

#        response = self.client.get("http://127.0.0.1:8000/manufacturers/?value_=1")
#        self.client.get(reverse("taxi:driver-list"), data=context)
        response = self.client.get(MANUFACTURER_URL + "?value_=1")
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__icontains="1"))
        )
