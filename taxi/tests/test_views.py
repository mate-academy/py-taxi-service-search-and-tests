from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from taxi.models import Manufacturer, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Test Manufacturer")
        Manufacturer.objects.create(name="Test Manufacturer 2")
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class CarSearchTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword123"
        )
        self.client.force_login(self.user)

        self.car_list_url = reverse("taxi:car-list")

        self.manufacturer = Manufacturer.objects.create(name="Toyota",
                                                        country="Japan")

        self.car_camry = Car.objects.create(
            model="Camry", manufacturer=self.manufacturer
        )
        self.car_corolla = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer
        )
        self.car_prius = Car.objects.create(
            model="Prius", manufacturer=self.manufacturer
        )

    def test_search_by_model_returns_correct_results(self):

        response = self.client.get(self.car_list_url, {"model": "Camry"})

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.car_camry.model)

        self.assertNotContains(response, self.car_corolla.model)
        self.assertNotContains(response, self.car_prius.model)

    def test_search_is_case_insensitive(self):

        response = self.client.get(self.car_list_url, {"model": "caMRy"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car_camry.model)

    def test_empty_search_returns_all_cars(self):
        response = self.client.get(self.car_list_url, {"model": ""})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car_camry.model)
        self.assertContains(response, self.car_corolla.model)
        self.assertContains(response, self.car_prius.model)


class DriverSearchTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_admin", password="test_password_123"
        )
        self.client.force_login(self.user)
        self.url = reverse("taxi:driver-list")

        self.driver_1 = get_user_model().objects.create_user(
            username="john_doe", password="password123",
            license_number="AAA12345"
        )
        self.driver_2 = get_user_model().objects.create_user(
            username="alex_smith", password="password123",
            license_number="BBB12345"
        )

    def test_search_by_username_is_case_insensitive(self):
        response = self.client.get(self.url, {"username": "JoHn"})
        self.assertEqual(response.status_code, 200)
        driver_list = list(response.context["driver_list"])
        self.assertIn(self.driver_1, driver_list)
        self.assertNotIn(self.driver_2, driver_list)

    def test_empty_driver_search_returns_all(self):
        response = self.client.get(self.url, {"username": ""})
        self.assertEqual(response.status_code, 200)
        driver_list = list(response.context["driver_list"])
        self.assertIn(self.driver_1, driver_list)
        self.assertIn(self.driver_2, driver_list)


class ManufacturerSearchTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_admin", password="test_password_123"
        )
        self.client.force_login(self.user)
        self.url = reverse("taxi:manufacturer-list")

        self.man_1 = Manufacturer.objects.create(name="Toyota",
                                                 country="Japan")
        self.man_2 = Manufacturer.objects.create(name="Ford",
                                                 country="USA")

    def test_search_by_name_is_case_insensitive(self):
        response = self.client.get(self.url, {"name": "tOyOtA"})
        self.assertEqual(response.status_code, 200)
        manufacturer_list = list(response.context["manufacturer_list"])
        self.assertIn(self.man_1, manufacturer_list)
        self.assertNotIn(self.man_2, manufacturer_list)

    def test_empty_manufacturer_search_returns_all(self):
        response = self.client.get(self.url, {"name": ""})
        self.assertEqual(response.status_code, 200)
        manufacturer_list = list(response.context["manufacturer_list"])
        self.assertIn(self.man_1, manufacturer_list)
        self.assertIn(self.man_2, manufacturer_list)
