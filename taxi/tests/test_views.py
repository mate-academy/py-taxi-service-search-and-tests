from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Car, Manufacturer


class PrivateCarListViewTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="1qazcde3"
        )
        self.client.force_login(self.driver)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="1qazcde3"
        )
        self.client.force_login(self.driver)

    def test_car_creation_and_assignment(self):
        form_data = {
            "username": "New_user",
            "password1": "zaq123edc",
            "password2": "zaq123edc",
            "license_number": "ABC12345",
            "first_name": "test first",
            "last_name": "test last",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        driver = get_user_model().objects.get(
            username=form_data["username"]
        )
        self.assertEqual(driver.first_name, "test first")
        self.assertEqual(driver.last_name, "test last")
        self.assertEqual(driver.username, "New_user")
        self.assertEqual(driver.license_number, "ABC12345")


class PrivateCarTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="1qazcde3"
        )
        self.client.force_login(self.driver)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="US",
        )
        self.car = Car.objects.create(
            model="Test Car",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_create_car(self):
        self.assertEqual(self.car.model, "Test Car")
        self.assertEqual(
            self.car.manufacturer, self.manufacturer
        )
        self.assertEqual(
            self.driver, self.car.drivers.all().first()
        )


class ManufacturerTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="1qazcde3"
        )
        self.client.force_login(self.driver)

    def test_create_manufacturer(self):
        manufacturer_test = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="US",
        )
        self.assertEqual(
            manufacturer_test.name, "Test Manufacturer"
        )
        self.assertEqual(manufacturer_test.country, "US")


class SearchViewsTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="1qazcde3",
            license_number="AQW12345",
        )
        self.client.force_login(self.driver)

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Honda",
            country="Japan"
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

        self.car1 = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Civic",
            manufacturer=self.manufacturer2
        )
        self.car3 = Car.objects.create(
            model="Focus",
            manufacturer=self.manufacturer3
        )

        get_user_model().objects.create_user(
            username="john_smith",
            password="pass123",
            license_number="ABC12345"
        )
        get_user_model().objects.create_user(
            username="john_doe",
            password="pass123",
            license_number="XYZ12345"
        )
        get_user_model().objects.create_user(
            username="michael99",
            password="pass123",
            license_number="LMN12345"
        )

    #  DRIVER SEARCH TESTS

    def test_driver_search_returns_matches(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "john"}
        )
        driver_list = (response.context.get("driver_list")
                       or response.context.get("object_list"))
        self.assertEqual(len(driver_list), 2)

    def test_driver_search_no_matches(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "zzz"}
        )
        driver_list = (response.context.get("driver_list")
                       or response.context.get("object_list"))
        self.assertEqual(len(driver_list), 0)

    def test_driver_search_empty_query(self):
        response = self.client.get(reverse("taxi:driver-list"))
        driver_list = (response.context.get("driver_list")
                       or response.context.get("object_list"))
        self.assertEqual(len(driver_list), 4)

    # CAR SEARCH TESTS

    def test_car_search_returns_matches(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "c"}
        )
        car_list = (response.context.get("car_list")
                    or response.context.get("object_list"))
        self.assertEqual(len(car_list), 3)  # Corolla, Civic

    def test_car_search_no_matches(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "zzz"}
        )
        car_list = (response.context.get("car_list")
                    or response.context.get("object_list"))
        self.assertEqual(len(car_list), 0)

    def test_car_search_empty_query(self):
        response = self.client.get(reverse("taxi:car-list"))
        car_list = (response.context.get("car_list")
                    or response.context.get("object_list"))
        self.assertEqual(len(car_list), 3)

    # MANUFACTURER SEARCH TESTS
    def test_manufacturer_search_returns_matches(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "o"}
        )
        manufacturer_list = (response.context.get("manufacturer_list")
                             or response.context.get("object_list"))
        self.assertEqual(len(manufacturer_list), 3)  # Toyota + Honda

    def test_manufacturer_search_no_matches(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "zzz"}
        )
        manufacturer_list = (response.context.get("manufacturer_list")
                             or response.context.get("object_list"))
        self.assertEqual(len(manufacturer_list), 0)

    def test_manufacturer_search_empty_query(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        manufacturer_list = (response.context.get("manufacturer_list")
                             or response.context.get("object_list"))
        self.assertEqual(len(manufacturer_list), 3)
