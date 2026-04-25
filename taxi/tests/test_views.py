from django.contrib.auth.models import User
from django.test import TestCase, Client
from taxi.models import Manufacturer, Car
from django.contrib.auth import get_user_model
from django.urls import reverse


class IndexTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)
        self.url = reverse("taxi:index")

    def test_status_code(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_login_required(self):
        self.client.logout()
        self.assertNotEqual(self.client.get(self.url).status_code, 200)

    def test_num_visits_increment(self):
        self.client.get(self.url)
        self.client.get(self.url)
        res = self.client.get(self.url)
        self.assertEqual(res.context["num_visits"], 3)


class ManufacturerListTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create(
            username="test",
            password="password",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="BMW", country="Germany")

        self.url = reverse("taxi:manufacturer-list")

    def test_status_code(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_login_required(self):
        self.client.logout()
        self.assertNotEqual(self.client.get(self.url).status_code, 200)

    def test_search_filter_works(self):
        res = self.client.get(self.url, {"name": "Toyota"})
        self.assertContains(res, "Toyota")
        self.assertNotContains(res, "BMW")

    def test_search_empty_returns_all(self):
        res = self.client.get(self.url, {"name": ""})
        self.assertContains(res, "Toyota")
        self.assertContains(res, "BMW")


class DriverListTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="password",
            license_number="ABC12345"
        )
        get_user_model().objects.create_user(
            username="Tim",
            password="password",
            license_number="CBA12345"
        )
        get_user_model().objects.create_user(
            username="Cook",
            password="password",
            license_number="BCD12345"
        )
        self.client.force_login(self.user)
        self.url = reverse("taxi:driver-list")

    def test_status_code(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_login_required(self):
        self.client.logout()
        self.assertNotEqual(self.client.get(self.url).status_code, 200)

    def test_search_filter_works(self):
        res = self.client.get(self.url, {"username": "Tim"})
        print(get_user_model().objects.all())
        self.assertContains(res, "Tim")
        self.assertNotContains(res, "Cook")


class CarListTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("taxi:car-list")

        self.user = get_user_model().objects.create(
            username="admin",
            password="123123",
            license_number="ABC12345"
        )

        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        car_1 = Car.objects.create(
            model="MX-6",
            manufacturer=manufacturer
        )
        car_2 = Car.objects.create(
            model="gt-86",
            manufacturer=manufacturer
        )

        car_1.drivers.add(self.user)
        car_2.drivers.add(self.user)

        self.client.force_login(self.user)

    def test_status_code(self):
        self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_login_required(self):
        self.client.logout()
        self.assertNotEqual(self.client.get(self.url).status_code, 200)

    def test_search_filter_work(self):
        res = self.client.get(self.url, {"model": "gt-86"})
        self.assertContains(res, "gt-86")
        self.assertNotContains(res, "MX-6")
