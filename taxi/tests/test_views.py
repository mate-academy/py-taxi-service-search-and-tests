from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="passwort123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="test", country="test")
        Manufacturer.objects.create(name="test2", country="test2")

        response = self.client.get(MANUFACTURER_LIST_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicCarTests(TestCase):
    def test_car_list_page_login_required(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_car_detail_page_login_required(self):
        url = reverse("taxi:car-detail", args=[1])
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="passwort123",
            license_number="TES12345",
        )
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        Car.objects.create(model="test", manufacturer=manufacturer)
        self.client.force_login(self.user)

    def test_car_list_retrieve(self):
        response = self.client.get(CAR_LIST_URL)
        car = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(car),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_detail_retrieve(self):
        url = reverse("taxi:car-detail", args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


class PublicDriverTests(TestCase):
    def test_driver_list_page_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_driver_detail_page_login_required(self):
        url = reverse("taxi:driver-detail", args=[1])
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            license_number="TES12345"
        )
        self.client.force_login(self.user)

    def test_driver_list_retrieve(self):
        response = self.client.get(DRIVER_LIST_URL)
        driver = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_detail_retrieve(self):
        url = reverse("taxi:driver-detail", args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
