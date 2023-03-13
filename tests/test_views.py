from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

import taxi.models
from taxi.models import Car, Manufacturer
from taxi.views import DriverCreateView

CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicUserTests(TestCase):

    def setUp(self) -> None:
        man = Manufacturer.objects.create(name="maa")
        car = Car.objects.create(manufacturer=man, model="text")
        self.url = reverse_lazy("taxi:car-detail", args=[car.id])

        driver = get_user_model().objects.create_user(
            username="name",
            password="12345"
        )

        self.drive_url = reverse_lazy("taxi:driver-detail", args=[driver.id])

    def test_client_car_list_and_detail(self):

        ls = self.client.get(CAR_LIST_URL)
        dt = self.client.get(self.url)

        self.assertNotEqual(ls.status_code, 200)
        self.assertNotEqual(dt.status_code, 200)

    def test_client_driver_list_and_detail(self):
        ls = self.client.get(DRIVER_LIST_URL)
        dt = self.client.get(self.drive_url)

        self.assertNotEqual(ls.status_code, 200)
        self.assertNotEqual(dt.status_code, 200)

    def test_manufacturer_list(self):
        res = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateUserTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="name",
            password="12345"
        )
        self.client.force_login(self.user)

        man = Manufacturer.objects.create(name="naa")
        car = Car.objects.create(manufacturer=man, model="text")

        self.car_url = reverse_lazy("taxi:car-detail", args=[car.id])
        self.drive_url = reverse_lazy(
            "taxi:driver-detail",
            args=[self.user.id]
        )

    def test_user_car_list_and_detail(self):

        ls = self.client.get(CAR_LIST_URL)
        dt = self.client.get(self.car_url)

        self.assertEqual(ls.status_code, 200)
        self.assertEqual(dt.status_code, 200)
        self.assertTemplateUsed(ls, "taxi/car_list.html")

    def test_user_driver_list_and_detail(self):
        ls = self.client.get(DRIVER_LIST_URL)
        dt = self.client.get(self.drive_url)

        self.assertEqual(ls.status_code, 200)
        self.assertEqual(dt.status_code, 200)
        self.assertTemplateUsed(ls, "taxi/driver_list.html")

    def test_user_manufacturer_list(self):
        ls = self.client.get(MANUFACTURER_LIST_URL)

        self.assertEqual(ls.status_code, 200)
        self.assertTemplateUsed(ls, "taxi/manufacturer_list.html")

    def test_create_driver_with_incorrect_license_number(self):
        form_data = {
            "username": "admin",
            "first_name": "name",
            "last_name": "last",
            "license_number": "not",
            "password1": "admin12345",
            "password2": "admin12345"
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        try:
            self.new_driver = get_user_model().objects.get(
                username=form_data["username"]
            )

        except taxi.models.Driver.DoesNotExist as error:
            self.assertTrue(error)

    def test_update_driver_with_incorrect_license_number(self):
        self.new_driver = get_user_model().objects.create_user(
            username="admin",
            password="12345",
            license_number="AAA12345"
        )

        form_data = {
            "license_number": "not",
        }
        self.client.force_login(self.new_driver)
        self.client.post(reverse(
            "taxi:driver-update",
            kwargs={"pk": self.new_driver.id}),
            data=form_data)

        self.new_driver = get_user_model().objects.get(pk=self.new_driver.id)

        self.assertNotEqual(self.new_driver.license_number, "not")
