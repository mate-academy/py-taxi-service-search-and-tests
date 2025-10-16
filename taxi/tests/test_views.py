from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer

DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
# User
TEST_USER_USERNAME = "testuser"
TEST_USER_PASSWORD = "testPass123"
TEST_USER_LICENSE = "TST12345"
TEST_USER_FIRST_NAME = "<NAME1>"
TEST_USER_LAST_NAME = "<SURNAME1>"

# Manufacturer
TEST_MANUFACTURER_NAME = "Test Motors"
TEST_MANUFACTURER_COUNTRY = "Test Country"

# Car
TEST_CAR_MODEL = "Audi A3"
TEST_CAR_LICENSE_PLATE = "AA1234BB"


class PublicDriverTests(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertEqual(res.status_code, 302)
        self.assertIn("/accounts/login/", res.url)


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="u1",
            password="pass",
            license_number="TST12345",
            first_name="<NAME>",
            last_name="<SURNAME>",
        )
        self.user2 = get_user_model().objects.create_user(
            username="u2",
            password="pass",
            license_number="TST54321",
            first_name="<NAME1>",
            last_name="<SURNAME1>",
        )
        self.client.force_login(self.user1)

    def test_retreat_drivers(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(len(drivers), 2)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_search_matching_query_returns_expected_drivers(self):
        """Test that searching by username returns expected driver(s)"""
        response = self.client.get(DRIVER_URL, {"username": TEST_USER_USERNAME})
        expected_drivers = Driver.objects.filter(username__icontains=TEST_USER_USERNAME)
        self.assertEqual(len(response.context["driver_list"]), len(expected_drivers))
        self.assertContains(response, self.user1.username)
        self.assertNotContains(response, self.user2.username)

    def test_driver_search_empty_query_returns_all_drivers(self):
        """test that empty username query returns all drivers (default)"""
        response = self.client.get(DRIVER_URL, {"username": ""})
        expected_drivers = Driver.objects.all()
        self.assertEqual(
            len(response.context["driver_list"]),
            len(expected_drivers)
        )
        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user2.username)

    def test_driver_search_non_matching_query_returns_no_results(self):
        """Test that searching by username with no matches returns empty results"""
        response = self.client.get(DRIVER_URL, {"username": "zz"})
        expected_drivers = Driver.objects.none()
        self.assertEqual(
            len(response.context["driver_list"]),
            len(expected_drivers)
        )
        for driver in response.context['driver_list']:
            self.assertNotEqual(driver, self.user1)
        self.assertNotContains(response, self.user2.username)


class PrivateCarViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model()
        cls.user = user.objects.create_user(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD,
            license_number=TEST_USER_LICENSE,
            first_name=TEST_USER_FIRST_NAME,
            last_name=TEST_USER_LAST_NAME,
        )
        cls.manufacturer = Manufacturer.objects.create(
            name=TEST_MANUFACTURER_NAME, country=TEST_MANUFACTURER_COUNTRY
        )
        cls.driver = user.objects.get(username=cls.user.username)
        cls.car = Car.objects.create(
            model=TEST_CAR_MODEL, manufacturer=cls.manufacturer
        )
        cls.car.drivers.add(cls.driver)

    def setUp(self):
        self.client.force_login(self.user)

    def test_car_search_matching_query_returns_expected_cars(self):
        """Test that searching by model returns expected car(s)"""
        response = self.client.get(CAR_URL, {"model": TEST_CAR_MODEL})
        expected_cars = Car.objects.filter(model__icontains=TEST_CAR_MODEL)
        self.assertEqual(len(response.context["car_list"]), len(expected_cars))
        self.assertContains(response, self.car.model)

    def test_car_search_empty_query_returns_all_cars(self):
        """test that empty model query returns all cars (default)"""
        response = self.client.get(CAR_URL, {"model": ""})
        expected_cars = Car.objects.all()
        self.assertEqual(
            len(response.context["car_list"]),
            len(expected_cars)
        )
        self.assertContains(response, self.car.model)

    def test_car_search_non_matching_query_returns_no_results(self):
        """Test that searching by model with no matches returns empty results"""
        response = self.client.get(CAR_URL, {"model": "zz"})
        expected_cars = Car.objects.none()
        self.assertEqual(
            len(response.context["car_list"]),
            len(expected_cars)
        )
        self.assertNotContains(response, self.car.model)

    # -----Update tests------

    def test_car_update_view(self):
        url = reverse("taxi:car-update", args=[self.car.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")
        self.assertContains(response, self.car.model)

    def test_car_update_view_post(self):
        url = reverse("taxi:car-update", args=[self.car.id])
        data = {
            "model": "Audi A4",
            "drivers": [self.driver.id],
            "manufacturer": self.manufacturer.id,
        }
        response = self.client.post(url, data)
        self.car.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.car.model, data.get("model"))

    # ---- DeleteView ----
    def test_car_delete_view_get(self):
        url = reverse("taxi:car-delete", args=[self.car.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_confirm_delete.html")
        self.assertContains(response, self.car.model)

    def test_car_delete_view_post(self):
        url = reverse("taxi:car-delete", args=[self.car.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertFalse(Car.objects.filter(id=self.car.id).exists())


class PrivateManufacturerViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model()
        cls.user = user.objects.create_user(
            username=TEST_USER_USERNAME,
            password=TEST_USER_PASSWORD,
            license_number=TEST_USER_LICENSE,
            first_name=TEST_USER_FIRST_NAME,
            last_name=TEST_USER_LAST_NAME,
        )
        cls.manufacturer = Manufacturer.objects.create(
            name=TEST_MANUFACTURER_NAME, country=TEST_MANUFACTURER_COUNTRY
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_driver_search_matching_query_returns_expected_drivers(self):
        """Test that searching by username returns expected manufacturer(s)"""
        response = self.client.get(MANUFACTURER_URL, {"name": TEST_MANUFACTURER_NAME})
        expected_manufacturers = Manufacturer.objects.filter(name__icontains=TEST_MANUFACTURER_NAME)
        self.assertEqual(len(response.context["manufacturer_list"]), len(expected_manufacturers))
        self.assertContains(response, self.manufacturer.name)

    def test_driver_search_empty_query_returns_all_drivers(self):
        """test that empty username query returns all manufacturers (default)"""
        response = self.client.get(MANUFACTURER_URL, {"name": ""})
        expected_manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            len(response.context["manufacturer_list"]),
            len(expected_manufacturers)
        )
        self.assertContains(response, self.manufacturer.name)

    def test_driver_search_non_matching_query_returns_no_results(self):
        """Test that searching by name with no matches returns empty results"""
        response = self.client.get(MANUFACTURER_URL, {"name": "zz"})
        expected_manufacturers = Manufacturer.objects.none()
        self.assertEqual(
            len(response.context["manufacturer_list"]),
            len(expected_manufacturers)
        )
        self.assertNotContains(response, self.manufacturer.name)

    # ----update tests----
    def test_manufacturer_update_view(self):
        url = reverse("taxi:manufacturer-update", args=[self.manufacturer.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")
        self.assertContains(response, self.manufacturer.name)

    def test_manufacturer_update_view_post(self):
        url = reverse("taxi:manufacturer-update", args=[self.manufacturer.id])
        data = {
            "name": "test_name2",
            "country": self.manufacturer.country,
        }
        response = self.client.post(url, data)
        self.manufacturer.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.manufacturer.name, data.get("name"))

    # ---- DeleteView ----
    def test_manufacturer_delete_view_get(self):
        url = reverse("taxi:manufacturer-delete", args=[self.manufacturer.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "taxi/manufacturer_confirm_delete.html"
        )
        self.assertContains(response, self.manufacturer.name)

    def test_manufacturer_delete_view_post(self):
        url = reverse("taxi:manufacturer-delete", args=[self.manufacturer.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertFalse(
            Manufacturer.objects.filter(id=self.manufacturer.id).exists()
        )
