from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class TestPublicManufacturerList(TestCase):
    def setUp(self):
        self.url = reverse("taxi:manufacturer-list")

    def test_car_list_view_login_required(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class TestPublicCarList(TestCase):
    def setUp(self):
        self.url = reverse("taxi:car-list")

    def test_car_list_view_login_required(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class TestPublicDriverList(TestCase):
    def setUp(self):
        self.url = reverse("taxi:driver-list")

    def test_car_list_view_login_required(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class TestPublicCarDetail(TestCase):
    def test_car_list_view_login_required(self):
        response = self.client.get("/cars/1")
        self.assertEqual(response.status_code, 301)


class TestPublicDriverDetail(TestCase):
    def test_car_list_view_login_required(self):
        response = self.client.get("/drivers/1")
        self.assertEqual(response.status_code, 301)


class TestManufacturerListSearch(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.superuser = (
            self.super_user
        ) = get_user_model().objects.create_superuser(
            username="superuser",
            password="password",
            first_name="first_name",
            last_name="last_name",
            license_number="license_number",
        )
        self.client.force_login(self.superuser)

        Manufacturer.objects.create(name="Porsche", country="Germany")

        self.base_url = "http://127.0.0.1:8000/manufacturers/?name="

    def test_search_no_manufacturers(self):
        search_value = "qwerty"
        response = self.client.get(f"{self.base_url}{search_value}")
        manufacturers = list(
            Manufacturer.objects.filter(name__icontains=search_value)
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]), manufacturers
        )

    def test_search_few_manufacturers(self):
        search_value = "porsche"
        response = self.client.get(f"{self.base_url}{search_value}")
        manufacturers = list(
            Manufacturer.objects.filter(name__icontains=search_value)
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]), manufacturers
        )


class TestCarListSearch(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.superuser = (
            self.super_user
        ) = get_user_model().objects.create_superuser(
            username="superuser",
            password="password",
            first_name="first_name",
            last_name="last_name",
            license_number="license_number",
        )
        self.client.force_login(self.superuser)

        manufacturer = Manufacturer.objects.create(
            name="Porsche", country="Germany"
        )
        Car.objects.create(
            model="911",
            manufacturer=manufacturer,
        )

        self.base_url = "http://127.0.0.1:8000/cars/?model="

    def test_search_no_manufacturers(self):
        search_value = "qwerty"
        response = self.client.get(f"{self.base_url}{search_value}")
        cars = list(Car.objects.filter(model__icontains=search_value))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), cars)

    def test_search_few_manufacturers(self):
        search_value = "911"
        response = self.client.get(f"{self.base_url}{search_value}")
        cars = list(Car.objects.filter(model__icontains=search_value))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), cars)


class TestDriverListSearch(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.superuser = (
            self.super_user
        ) = get_user_model().objects.create_superuser(
            username="superuser",
            password="password",
            first_name="first_name",
            last_name="last_name",
            license_number="license_number",
        )
        self.client.force_login(self.superuser)

        self.base_url = "http://127.0.0.1:8000/drivers/?username="

    def test_search_no_manufacturers(self):
        search_value = "qwerty"
        response = self.client.get(f"{self.base_url}{search_value}")
        drivers = list(Driver.objects.filter(username__icontains=search_value))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), drivers)

    def test_search_few_manufacturers(self):
        search_value = "superuser"
        response = self.client.get(f"{self.base_url}{search_value}")
        drivers = list(Driver.objects.filter(username__icontains=search_value))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), drivers)
