from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car
from taxi.forms import DriverSearchForm, DriverCreationForm


HOME_URL = reverse("taxi:index")
MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
DRIVERS_URL = reverse("taxi:driver-list")
CARS_URL = reverse("taxi:car-list")


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin",
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver",
            license_number="JON26231",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Audi", country="Germany"
        )
        self.car = Car.objects.create(
            model="A6",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_driver_licence_listed(self):
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)

    def test_car_model_manufacturer_listed(self):
        url = reverse("admin:taxi_car_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.car.model)
        self.assertContains(response, self.car.manufacturer.name)

    def test_manufacturer_name_country_listed(self):
        url = reverse("admin:taxi_manufacturer_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.manufacturer.name)
        self.assertContains(response, self.manufacturer.country)

    def test_driver_detail_license_listed(self):
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)

        self.assertContains(response, self.driver.license_number)


class TestDriverUsernameSearchForm(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin",
        )
        self.client.force_login(self.user)
        get_user_model().objects.create_user(
            username="johnson",
            password="johnson",
            license_number="BON26231",
        )
        get_user_model().objects.create_user(
            username="john",
            password="john",
            license_number="ION26232",
        )

    def test_driver_username_search_form(self):
        form_data = {"username": "admin"}
        form = DriverSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_driver_username_search_form_username_search(self):
        form_data = {"username": "john"}
        url = reverse("taxi:driver-list")
        response = self.client.get(url, data=form_data)
        self.assertContains(response, form_data["username"])
        self.assertNotContains(response, "mike")


class TestDriverCreationForm(TestCase):
    def test_driver_creation_form_with_valid_license_number(self):
        form_data = {
            "username": "admin1",
            "password1": "bohatov1",
            "password2": "bohatov1",
            "license_number": "JON26234",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_without_license_number(self):
        form_data = {
            "username": "admin",
            "password1": "123456",
            "password2": "123456",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_license_number_too_short(self):
        form_data = {
            "username": "admin",
            "password1": "123456",
            "password2": "123456",
            "license_number": "JON2623",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_license_number_too_long(self):
        form_data = {
            "username": "admin",
            "password1": "123456",
            "password2": "123456",
            "license_number": "JON262334",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_license_number_with_only_digits(self):
        form_data = {
            "username": "admin",
            "password1": "123456",
            "password2": "123456",
            "license_number": "12345678",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_driver_creation_form_license_number_with_only_letters(self):
        form_data = {
            "username": "admin",
            "password1": "123456",
            "password2": "123456",
            "license_number": "ABCDEFGHI",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)


class ModelTests(TestCase):
    def setUp(self) -> None:
        username = "admin"
        password = "123456"
        license_number = "JON26231"
        first_name = "Jon"
        last_name = "Doe"
        self.driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            license_number=license_number,
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Audi", country="Germany"
        )

    def test_manufacturer_str_method(self):
        manufacturer = self.manufacturer
        self.assertEqual(str(manufacturer), "Audi Germany")

    def test_driver_str(self):
        driver = self.driver
        self.assertEqual(
            str(self.driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})",
        )

    def test_create_author_with_licence(self):
        driver = self.driver
        self.assertEqual(driver.license_number, "JON26231")

    def test_car_str_method(self):
        car = Car.objects.create(model="A6", manufacturer=self.manufacturer)
        self.assertEqual(str(car), "A6")


class TestViewsStatusCode(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get(HOME_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturers_page_status_code(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_drivers_page_status_code(self):
        response = self.client.get(DRIVERS_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_cars_page_status_code(self):
        response = self.client.get(CARS_URL)
        self.assertNotEqual(response.status_code, 200)


class TestDriversListView(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin",
        )
        self.client.force_login(self.user)
