from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicAccessTests(TestCase):

    def test_login_required(self):
        response = [
            self.client.get(MANUFACTURER_URL),
            self.client.get(CAR_URL),
            self.client.get(DRIVER_URL)
        ]
        for test in response:
            self.assertNotEqual(test.status_code, 200)


class PrivateTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="BMW",
            country="Germany",)
        Manufacturer.objects.create(
            name="ZAZAUTO",
            country="Ukrane",
        )

        response = self.client.get(MANUFACTURER_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_ordered_by_name(self):
        response = self.client.get(MANUFACTURER_URL)
        main_list = Manufacturer.objects.all().order_by("name")
        manufacturer_context = response.context["manufacturer_list"]

        self.assertEqual(
            list(manufacturer_context),
            list(main_list[: len(manufacturer_context)]),
        )

    def test_retrieve_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user123test",
            "password2": "user123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ADM56984",
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])

    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",)
        Car.objects.create(
            model="BMW 5",
            manufacturer=manufacturer, )
        Car.objects.create(
            model="BMW 7",
            manufacturer=manufacturer,
        )

        response = self.client.get(CAR_URL)

        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_detail_driver(self):
        response = self.client.get(reverse("taxi:driver-detail", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_detail_car(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany", )
        Car.objects.create(
            model="BMW 5",
            manufacturer=manufacturer, )
        Car.objects.create(
            model="BMW 7",
            manufacturer=manufacturer,
        )
        response = self.client.get(reverse("taxi:car-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")
