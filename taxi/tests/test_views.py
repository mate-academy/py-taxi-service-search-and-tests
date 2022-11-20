from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")
HOME_PAGE_URL = reverse("taxi:index")
LOGIN_PAGE_URL = reverse("login")


class PublicAccessTests(TestCase):
    def test_login_required_for_manufacturer(self):
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_driver(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_car(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_for_home_page(self):
        response = self.client.get(HOME_PAGE_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get(LOGIN_PAGE_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")


class PrivateAccessTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test", password="password123", license_number="TOK12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )

        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        response = self.client.get(MANUFACTURER_LIST_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_driver(self):
        get_user_model().objects.create(
            username="testik",
            first_name="testik first",
            last_name="testik last",
            password="test_pass123",
            license_number="TES12345",
        )

        response = self.client.get(DRIVER_LIST_URL)

        drivers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class SearchTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123",
        )
        self.client.force_login(self.user)

    def test_car_search(self):
        response = self.client.get(CAR_LIST_URL + "?model=test")
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model__icontains="test")),
        )

    def test_manufacturer_search(self):
        response = self.client.get(MANUFACTURER_LIST_URL + "?name=test")
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__icontains="test")),
        )

    def test_driver_search(self):
        response = self.client.get(DRIVER_LIST_URL + "?username=test")
        self.assertEqual(
            list(response.context["driver_list"]),
            list(Driver.objects.filter(username__icontains="test")),
        )
