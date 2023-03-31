from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="pass12345word",
        )

        self.client.force_login(self.user)

        Driver.objects.create(
            username="Driver1",
            first_name="Bob",
            last_name="Qwert",
            license_number="QWE12345"
        )
        Driver.objects.create(
            username="Driver2",
            first_name="Alice",
            last_name="Ukjbsd",
            license_number="YUI87537"
        )
        Driver.objects.create(
            username="Driver3",
            first_name="Tom",
            last_name="Hold",
            license_number="QGD73920"
        )
        Driver.objects.create(
            username="Driver4",
            first_name="Ann",
            last_name="Hloya",
            license_number="UFR26186"
        )

    def test_retrieve_driver(self):
        res = self.client.get(DRIVER_LIST_URL)
        drivers = Driver.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_search_driver_by_username(self):
        res = self.client.get(DRIVER_LIST_URL + "?username=a")

        drivers = Driver.objects.filter(username__icontains="a")
        self.assertEqual(list(res.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "driver_user",
            "password1": "paSSwor12",
            "password2": "paSSwor12",
            "first_name": "New Driver",
            "last_name": "Driver",
            "license_number": "OIU12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
