from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverSearchForm, CarSearchForm, ManufacturerSearchForm
from taxi.models import Manufacturer, Car, Driver

# URL constants
INDEX_URL = reverse("taxi:index")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

    def test_get_context_data_includes_search_form(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"], ManufacturerSearchForm)

    def test_get_queryset_with_search_filter(self):
        Manufacturer.objects.create(name="test1", country="testcountry")
        Manufacturer.objects.create(name="test2", country="testcountry")
        Manufacturer.objects.create(name="test3", country="testcountry")

        response = self.client.get(MANUFACTURER_URL, {"name": "test1"})
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
        self.assertEqual(
            response.context["manufacturer_list"][0].name, "test1")

    def test_get_queryset_without_search_returns_all(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")

        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(len(response.context["manufacturer_list"]), 2)

    def test_get_queryset_with_non_matching_search_returns_empty(self):
        """Test that non-matching search query returns no results"""
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")
        Manufacturer.objects.create(name="Mercedes", country="Germany")

        response = self.client.get(MANUFACTURER_URL, {"name": "NonExistentManufacturer"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 0)


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )

    def test_get_context_data_includes_search_form(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(response.context["search_form"], CarSearchForm)

    def test_get_queryset_with_search_filter(self):
        Car.objects.create(
            model="BMW X5",
            manufacturer=self.manufacturer)
        Car.objects.create(
            model="Audi A4",
            manufacturer=self.manufacturer)
        Car.objects.create(
            model="Mercedes C-Class",
            manufacturer=self.manufacturer)

        response = self.client.get(CAR_URL, {"model": "BMW"})
        self.assertEqual(len(response.context["car_list"]), 1)
        self.assertEqual(response.context["car_list"][0].model, "BMW X5")

    def test_get_queryset_with_empty_search(self):
        Car.objects.create(model="BMW X5", manufacturer=self.manufacturer)
        Car.objects.create(model="Audi A4", manufacturer=self.manufacturer)

        response = self.client.get(CAR_URL)
        self.assertEqual(len(response.context["car_list"]), 2)

    def test_get_queryset_with_non_matching_search_returns_empty(self):
        """Test that non-matching search query returns no results"""
        Car.objects.create(model="BMW X5", manufacturer=self.manufacturer)
        Car.objects.create(model="Audi A4", manufacturer=self.manufacturer)
        Car.objects.create(model="Mercedes C-Class", manufacturer=self.manufacturer)

        response = self.client.get(CAR_URL, {"model": "NonExistentModel"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 0)

    def test_select_related_optimization(self):
        Car.objects.create(model="Test Car", manufacturer=self.manufacturer)

        response = self.client.get(CAR_URL)
        car_from_context = response.context["car_list"][0]

        with self.assertNumQueries(0):
            manufacturer_name = car_from_context.manufacturer.name
            self.assertEqual(manufacturer_name, "Test Manufacturer")


class DriverListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test1234",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

    def test_get_context_data_includes_search_form_and_username(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertIn("username", response.context)
        self.assertIsInstance(
            response.context["search_form"], DriverSearchForm)

    def test_get_context_data_with_username_parameter(self):
        response = self.client.get(DRIVER_URL, {"username": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["username"], "test")

    def test_get_queryset_with_search_filter(self):
        Driver.objects.create_user(
            username="john_doe", password="test123", license_number="LIC00001"
        )
        Driver.objects.create_user(
            username="jane_smith", password="test123", license_number="LIC00002"
        )
        Driver.objects.create_user(
            username="bob_johnson", password="test123", license_number="LIC00003"
        )

        response = self.client.get(DRIVER_URL, {"username": "john"})
        # Only "john_doe" contains "john" in username
        self.assertEqual(len(response.context["driver_list"]), 2)
        self.assertEqual(response.context["driver_list"][0].username, "john_doe")

    def test_get_queryset_without_search_returns_all(self):
        Driver.objects.create_user(
            username="driver1", password="test123", license_number="LIC00001"
        )
        Driver.objects.create_user(
            username="driver2", password="test123", license_number="LIC00002"
        )

        response = self.client.get(DRIVER_URL)
        # 3 drivers total: 2 created + 1 from setUp (self.user)
        self.assertEqual(len(response.context["driver_list"]), 3)

    def test_get_queryset_with_non_matching_search_returns_empty(self):
        """Test that non-matching search query returns no results"""
        Driver.objects.create_user(
            username="john_doe", password="test123", license_number="LIC00001"
        )
        Driver.objects.create_user(
            username="jane_smith", password="test123", license_number="LIC00002"
        )
        Driver.objects.create_user(
            username="bob_johnson", password="test123", license_number="LIC00003"
        )

        response = self.client.get(DRIVER_URL, {"username": "NonExistentUsername"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 0)


class DriverDetailViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test1234",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )

    def test_prefetch_related_optimization(self):
        driver = Driver.objects.create_user(
            username="testdriver", password="test123", license_number="LIC00004"
        )
        car1 = Car.objects.create(
            model="Car 1",
            manufacturer=self.manufacturer)
        car2 = Car.objects.create(
            model="Car 2",
            manufacturer=self.manufacturer)
        driver.cars.add(car1, car2)

        response = self.client.get(
            reverse("taxi:driver-detail", args=[driver.id]))
        self.assertEqual(response.status_code, 200)

        driver_from_context = response.context["driver"]

        with self.assertNumQueries(0):
            cars = list(driver_from_context.cars.all())
            self.assertEqual(len(cars), 2)

            for car in cars:
                manufacturer_name = car.manufacturer.name
                self.assertEqual(manufacturer_name, "Test Manufacturer")


class ToggleAssignToCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )
        self.car = Car.objects.create(
            model="Test Car",
            manufacturer=self.manufacturer)

    def test_toggle_assign_adds_driver_to_car(self):
        self.assertNotIn(self.car, self.user.cars.all())

        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.id])
        )

        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertIn(self.car, self.user.cars.all())
        self.assertEqual(
            response.url, reverse("taxi:car-detail", args=[self.car.id]))

    def test_toggle_assign_removes_driver_from_car(self):
        self.user.cars.add(self.car)
        self.assertIn(self.car, self.user.cars.all())

        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.id])
        )

        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertNotIn(self.car, self.user.cars.all())
        self.assertEqual(
            response.url, reverse("taxi:car-detail", args=[self.car.id]))
