from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")
PAGINATION = 5


class PublicLoginTest(TestCase):
    def test_manufacturer_list_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_driver_list_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_car_list_login_required(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_index_page_login_required(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertNotEqual(response.status_code, 200)


class ManufacturerListTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="Bob",
            password="<PASSWORD>"
        )
        self.client.force_login(self.driver)
        Manufacturer.objects.create(
            name="<NAME>",
            country="USA"
        )
        Manufacturer.objects.create(
            name="<NAME_SECOND>",
            country="JAPAN"
        )
        Manufacturer.objects.create(
            name="<NAME_THIRD>",
            country="KOREA"
        )
        Manufacturer.objects.create(
            name="<NAME_FORTH>",
            country="KOREA"
        )
        Manufacturer.objects.create(
            name="<NAME_FIFTH>",
            country="KOREA"
        )
        Manufacturer.objects.create(
            name="<NAME_SIX>",
            country="KOREA"
        )

    def test_retrieve_manufacturer_list(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        man_list = Manufacturer.objects.all().order_by("name")
        manufacturer_context = response.context["manufacturer_list"]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertEqual(
            len(response.context["manufacturer_list"]), PAGINATION
        )
        self.assertEqual(
            list(manufacturer_context),
            list(man_list[: len(manufacturer_context)]),
        )


class CarListAndDetailTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="Bob",
            password="<PASSWORD>"
        )
        self.client.force_login(self.driver)
        self.manufacturer = Manufacturer.objects.create(
            name="<NAME_SECOND>",
            country="JAPAN"
        )
        Car.objects.create(
            model="Ford",
            manufacturer=self.manufacturer
        )
        Car.objects.create(
            model="Renaught",
            manufacturer=self.manufacturer
        )
        Car.objects.create(
            model="Cherry",
            manufacturer=self.manufacturer
        )

    def test_retrieve_car_list(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_car_detail(self):
        response = self.client.get(reverse("taxi:car-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")


class DriverListAndDetailTest(TestCase):
    def setUp(self) -> None:
        self.first_driver = get_user_model().objects.create_user(
            username="Bob",
            password="<PASSWORD>",
            first_name="Bob",
            last_name="Bobul",
            license_number="TES12346"
        )
        get_user_model().objects.create_user(
            username="Ivan",
            password="Test123",
            first_name="Vano",
            last_name="Vanov",
            license_number="TES12341"
        )
        get_user_model().objects.create_user(
            username="Frank",
            password="Test123",
            first_name="Frank",
            last_name="Frankov",
            license_number="TES12349"
        )
        self.client.force_login(self.first_driver)

    def test_retrieve_driver_list(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_driver_detail(self):
        response = self.client.get(reverse("taxi:driver-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")
