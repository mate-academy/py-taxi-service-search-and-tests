from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTests(TestCase):
    """Tests that login required to enter this page"""
    def test_manufacturer_list_login_required(self):
        result = self.client.get(MANUFACTURER_URL)

        self.assertNotEquals(result.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="test_one", country="Testland")
        Manufacturer.objects.create(name="test_two", country="Testonia")

        response = self.client.get(MANUFACTURER_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(name="test_one", country="Testland")
        name_for_search = "test_one"
        response = self.client.get(
            MANUFACTURER_URL,
            {"name": name_for_search}
        )
        self.assertEqual(response.status_code, 200)

        manufacturer_for_search = Manufacturer.objects.filter(name__icontains=name_for_search)
        self.assertQuerysetEqual(response.context["manufacturer_list"], manufacturer_for_search)


class PublicCarTests(TestCase):
    """Tests that login required to enter this page"""
    def test_car_list_login_required(self):
        result = self.client.get(CAR_URL)

        self.assertNotEquals(result.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(name="test_one", country="Testland")
        Car.objects.create(
            model="test",
            manufacturer=manufacturer
        )
        Car.objects.create(
            model="test_second",
            manufacturer=manufacturer
        )

        response = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(name="test_one", country="Testland")
        Car.objects.create(
            model="test_model",
            manufacturer=manufacturer
        )
        model_for_search = "test_model"
        response = self.client.get(CAR_URL, {"model": model_for_search})

        self.assertEqual(response.status_code, 200)

        car_for_search = Car.objects.filter(model__icontains=model_for_search)
        self.assertQuerysetEqual(response.context["car_list"], car_for_search)


class PublicDriverTests(TestCase):
    """Tests that login required to enter this page"""
    def test_driver_list_login_required(self):
        result = self.client.get(DRIVER_URL)

        self.assertNotEquals(result.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        get_user_model().objects.create_user(
            username="test_first",
            password="password1234",
            license_number="QWE90009"
        )
        get_user_model().objects.create_user(
            username="test_second",
            password="password1234",
            license_number="ZXC70007"
        )
        response = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_driver_by_username(self):
        get_user_model().objects.create_user(
            username="test_first",
            password="password1234",
            license_number="QWE90009"
        )

        username_for_search = "test_first"
        response = self.client.get(DRIVER_URL, {"username": username_for_search})

        self.assertEqual(response.status_code, 200)

        driver_for_search = Driver.objects.filter(username__icontains=username_for_search)
        self.assertQuerysetEqual(response.context["driver_list"], driver_for_search)
