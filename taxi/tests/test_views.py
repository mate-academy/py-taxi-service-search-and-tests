from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    @classmethod
    def setUpTestData(cls) -> None:
        cls.manufacturer_1 = Manufacturer.objects.create(name="Skoda")
        cls.manufacturer_2 = Manufacturer.objects.create(name="Audi")
        cls.manufacturer_3 = Manufacturer.objects.create(name="sKODA")

    def test_retrieve_manufacturers(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertEqual(res.status_code, 200)
        self.assertCountEqual(
            list(res.context["manufacturer_list"]),
            [self.manufacturer_1, self.manufacturer_2, self.manufacturer_3]
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_search_finds_matches(self):
        response = self.client.get(f"{MANUFACTURER_URL}?name=Sk")
        result = [self.manufacturer_1, self.manufacturer_3]
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            result
        )
        self.assertEqual(
            response.context["search_form"].initial["name"],
            "Sk"
        )

    def test_empty_search_returns_all(self):
        response = self.client.get(f"{MANUFACTURER_URL}?name=")
        self.assertCountEqual(
            list(response.context["manufacturer_list"]),
            [self.manufacturer_1, self.manufacturer_2, self.manufacturer_3]
        )
        self.assertEqual(
            response.context["search_form"].initial["name"],
            ""
        )

    def test_search_no_results(self):
        response = self.client.get(f"{MANUFACTURER_URL}?name=WAG")
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            []
        )


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    @classmethod
    def setUpTestData(cls) -> None:
        cls.manufacturer = Manufacturer.objects.create(name="Skoda")
        cls.car_1 = Car.objects.create(
            model="X5",
            manufacturer=cls.manufacturer
        )
        cls.car_2 = Car.objects.create(
            model="Escort",
            manufacturer=cls.manufacturer
        )
        cls.car_3 = Car.objects.create(
            model="FabiaeS",
            manufacturer=cls.manufacturer
        )

    def test_retrieve_cars(self):
        res = self.client.get(CAR_URL)
        self.assertEqual(res.status_code, 200)
        self.assertCountEqual(
            list(res.context["car_list"]),
            [self.car_1, self.car_2, self.car_3]
        )
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_search_finds_matches(self):
        response = self.client.get(f"{CAR_URL}?model=ES")
        result = [self.car_2, self.car_3]
        self.assertEqual(
            list(response.context["car_list"]),
            result
        )
        self.assertEqual(
            response.context["search_form"].initial["model"],
            "ES"
        )

    def test_empty_search_returns_all(self):
        response = self.client.get(f"{CAR_URL}?model=")
        self.assertEqual(
            list(response.context["car_list"]),
            [self.car_1, self.car_2, self.car_3]
        )
        self.assertEqual(
            response.context["search_form"].initial["model"],
            ""
        )

    def test_search_no_results(self):
        response = self.client.get(f"{CAR_URL}?model=WAG")
        self.assertEqual(
            list(response.context["car_list"]),
            []
        )


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    @classmethod
    def setUpTestData(cls) -> None:
        cls.driver_1 = Driver.objects.create(
            username="pedro_123",
            first_name="test",
            last_name="testovich",
            license_number="ASD35623"
        )
        cls.driver_2 = Driver.objects.create(
            username="DRO2345",
            first_name="test",
            last_name="testovich",
            license_number="HKC45001"
        )
        cls.driver_3 = Driver.objects.create(
            username="ivan12",
            first_name="test",
            last_name="testovich",
            license_number="XNL12406"
        )

    def test_retrieve_drivers(self):
        res = self.client.get(DRIVER_URL)
        self.assertEqual(res.status_code, 200)
        self.assertCountEqual(
            list(res.context["driver_list"]),
            [self.driver_1, self.driver_2, self.driver_3, self.user]
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_search_finds_matches(self):
        response = self.client.get(f"{DRIVER_URL}?username=Dr")
        result = [self.driver_1, self.driver_2]
        self.assertCountEqual(
            list(response.context["driver_list"]),
            result
        )
        self.assertEqual(
            response.context["search_form"].initial["username"],
            "Dr"
        )

    def test_empty_search_returns_all(self):
        response = self.client.get(f"{DRIVER_URL}?username=")
        self.assertCountEqual(
            list(response.context["driver_list"]),
            [self.driver_1, self.driver_2, self.driver_3, self.user]
        )
        self.assertEqual(
            response.context["search_form"].initial["username"],
            ""
        )

    def test_search_no_results(self):
        response = self.client.get(f"{DRIVER_URL}?username=WAG")
        self.assertEqual(
            list(response.context["driver_list"]),
            []
        )
