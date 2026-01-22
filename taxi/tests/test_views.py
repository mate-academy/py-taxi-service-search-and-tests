from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class TestManufacturerPublic(TestCase):

    def test_login_required(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(res.status_code, 200)


class TestManufacturerPrivate(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country",
        )
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

        manufacturer = Manufacturer.objects.all()
        self.assertEqual(list(response.context["manufacturer_list"]),
                         list(manufacturer))

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class TestCarPublic(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(res.status_code, 200)


class TestCarPrivate(TestCase):
    def setUp(self):

        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        self.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country",
        )
        Car.objects.create(
            model="test_model",
            manufacturer=self.manufacturer,
        )
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

        car = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(car))

        self.assertTemplateUsed(response, "taxi/car_list.html")


class TestDriverPublic(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(res.status_code, 200)


class TestDriverPrivate(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        Driver.objects.create(
            username="test_driver",
            password="test_password",
            license_number="AAA11111",
        )
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        driver = Driver.objects.all()
        self.assertEqual(list(response.context["driver_list"]), list(driver))
