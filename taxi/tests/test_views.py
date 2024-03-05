from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="qwer1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="test1", country="USA")
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="qwer1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(name="test1", country="USA")
        Car.objects.create(manufacturer=manufacturer, model="test")
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="qwer1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)


class CarListViewSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="qwer1234"
        )
        self.client.login(username="user", password="qwer1234")
        mercedes_manufacturer = Manufacturer.objects.create(name="Mercedes")

        Car.objects.create(
            model="Mercedes",
            manufacturer=mercedes_manufacturer
        )

    def test_car_list_view_with_search(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "Mercedes"})
        self.assertEqual(response.status_code, 200)
