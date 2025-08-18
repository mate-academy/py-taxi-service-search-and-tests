from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self) -> None:
        driver = Driver.objects.create(
            username="reinvvay",
            first_name="Andrii",
            last_name="Roman"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        car = Car.objects.create(
            model="Model Y",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)


class AdminTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin"
        )
        self.client.force_login(self.admin_user)
        self.driver = get_user_model().objects.create_user(
            username="reinvvay",
            password="reinvvay",
            license_number="TAB12345"
        )

    def test_username_listed(self) -> None:
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.username)

    def test_license_number_listed(self) -> None:
        url = reverse("admin:taxi_driver_changelist")
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)

    def test_license_number_detail_listed(self) -> None:
        url = reverse("admin:taxi_driver_change", args=[self.driver.id])
        response = self.client.get(url)
        self.assertContains(response, self.driver.license_number)


class ViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="reinvvay",
            password="reinvvay",
            license_number="TAB12345"
        )
        self.client.force_login(self.user)

    def test_login_required(self) -> None:
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_manufacturer_list(self) -> None:
        Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_drivers_list(self) -> None:
        Driver.objects.create(
            username="test1",
            password="test1",
            license_number="-"
        )
        Driver.objects.create(
            username="test2",
            password="test2",
            license_number="--"
        )
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_cars_list(self) -> None:
        first_manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        second_manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Car.objects.create(
            model="Model Y",
            manufacturer=first_manufacturer
        )
        Car.objects.create(
            model="M5",
            manufacturer=second_manufacturer
        )
        cars = Car.objects.all()
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_driver_detail_list(self):
        driver = Driver.objects.create_user(
            username="test1",
            password="test12345",
            license_number="ABC12345"
        )
        url = reverse("taxi:driver-detail", args=[driver.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, driver.username)


class FormTest(TestCase):
    def test_form_is_valid(self) -> None:
        form_data = {
            "username": "reinvvay",
            "password1": "admin543",
            "password2": "admin543",
            "license_number": "ABC12345",
            "first_name": "Andrii",
            "last_name": "Roman"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_incorrect_license_number(self) -> None:
        form_data = {
            "username": "reinvvay",
            "password1": "admin543",
            "password2": "admin543",
            "license_number": "incorrect",
            "first_name": "Andrii",
            "last_name": "Roman"
        }
        form = DriverCreationForm(data=form_data)
        self.assertIn("license_number", form.errors)

    def test_incorrect_password(self) -> None:
        form_data = {
            "username": "reinvvay",
            "password1": "admin534",
            "password2": "admin543",
            "license_number": "ABC12345",
            "first_name": "Andrii",
            "last_name": "Roman"
        }
        form = DriverCreationForm(data=form_data)
        self.assertIn("password2", form.errors)

    def test_incorrect_username(self) -> None:
        form_data = {
            "username": "",
            "password1": "admin543",
            "password2": "admin543",
            "license_number": "ABC12345",
            "first_name": "Andrii",
            "last_name": "Roman"
        }
        form = DriverCreationForm(data=form_data)
        self.assertIn("username", form.errors)
