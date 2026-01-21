from http import client
from bs4 import BeautifulSoup

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="Manufacturer 1",
            country="test_country",
        )
        res = self.client.get(MANUFACTURER_URL)
        self.assertEqual(res.status_code, 200)
        manufacturer_list = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]), list(manufacturer_list)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer-list.html")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        get_user_model().objects.create_user(
            username="test_user",
            password="<PASSWORD>",
            license_number="test_license_number",
        )
        res = self.client.get(DRIVER_URL)
        self.assertEqual(res.status_code, 200)
        driver_list = get_user_model().objects.all()
        self.assertEqual(list(res.context["driver_list"]), list(driver_list))
        self.assertTemplateUsed(res, "taxi/driver_list.html")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Manufacturer 1",
            country="test_country",
        )
        Car.objects.create(
            model="test_model",
            manufacturer=manufacturer,
        )
        res = self.client.get(CAR_URL)
        self.assertEqual(res.status_code, 200)
        car_list = Car.objects.all()
        self.assertEqual((list(res.context["car_list"])), list(car_list))
        self.assertTemplateUsed(res, "taxi/car_list.html")


class DriverSearchTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_model = get_user_model()

        cls.driver1 = cls.user_model.objects.create_user(
            username="driver1",
            password="test123",
            license_number="ABC123"
        )

        cls.driver2 = cls.user_model.objects.create_user(
            username="test_driver",
            password="test123",
            license_number="XYZ789"
        )

        cls.driver3 = cls.user_model.objects.create_user(
            username="another_driver",
            password="test123",
            license_number="LMN456"
        )

    def setUp(self):
        self.client.login(username="driver1", password="test123")

    def test_driver_list_view_displays_all_drivers(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver1")
        self.assertContains(response, "test_driver")
        self.assertContains(response, "another_driver")

    def test_driver_list_view_filters_by_username(self):
        url = reverse("taxi:driver-list") + "?username=test"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "driver1")
        self.assertContains(response, "test_driver")
        self.assertNotContains(response, "another_driver")

    def test_search_form_is_rendered(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<input type="text" name="username"')
