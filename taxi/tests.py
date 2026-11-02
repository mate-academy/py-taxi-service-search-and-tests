from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car


class ModelTest(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_str(self):
        driver = get_user_model().objects.create(
            username="test_driver",
            first_name="John",
            last_name="Doe"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        car = Car.objects.create(
            model="Camry",
            manufacturer=manufacturer,
        )
        self.assertEqual(str(car), car.model)

    def test_create_driver_with_license_number(self):
        username = "test_driver"
        password = "test_password123"
        license_number = "ABC12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertEqual(driver.license_number, license_number)
        self.assertTrue(driver.check_password(password))


class FormTest(TestCase):
    def test_driver_create_form(self):
        form_data = {
            "username": "test_driver",
            "first_name": "John",
            "last_name": "Doe",
            "license_number": "ABC12345",
            "password1": "TestPass12345!",
            "password2": "TestPass12345!",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_license_number_validation(self):
        invalid_license_numbers = [
            "ABC1234",
            "ABC123456",
            "abc12345",
            "12C12345",
            "ABC1234A",
        ]
        for license_number in invalid_license_numbers:
            form = DriverLicenseUpdateForm(
                data={"license_number": license_number}
            )
            self.assertFalse(form.is_valid())


class PublicViewTests(TestCase):
    def test_login_required(self):
        urls = [
            reverse("taxi:index"),
            reverse("taxi:manufacturer-list"),
            reverse("taxi:car-list"),
            reverse("taxi:driver-list"),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)


class PrivateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_driver",
            password="test_password123",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_lists(self):
        urls = [
            reverse("taxi:manufacturer-list"),
            reverse("taxi:car-list"),
            reverse("taxi:driver-list"),
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_search_manufacturers(self):
        manufacturer_1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        manufacturer_2 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Toy"}
        )
        self.assertIn(manufacturer_1, response.context["manufacturer_list"])
        self.assertNotIn(manufacturer_2, response.context["manufacturer_list"])

    def test_search_cars(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        car1 = Car.objects.create(model="Camry", manufacturer=manufacturer)
        car2 = Car.objects.create(model="Corolla", manufacturer=manufacturer)
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Cam"}
        )
        self.assertIn(car1, response.context["car_list"])
        self.assertNotIn(car2, response.context["car_list"])

    def test_search_drivers(self):
        driver2 = get_user_model().objects.create_user(
            username="john_wick",
            password="test_password123",
            license_number="DEF12345",
        )
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "john"}
        )
        self.assertIn(driver2, response.context["driver_list"])
        self.assertNotIn(self.user, response.context["driver_list"])

    def test_toggle_assign_to_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        car = Car.objects.create(model="Camry", manufacturer=manufacturer)
        self.client.get(reverse("taxi:toggle-car-assign", args=[car.id]))
        self.assertIn(car, self.user.cars.all())
        self.client.get(reverse("taxi:toggle-car-assign", args=[car.id]))
        self.assertNotIn(car, self.user.cars.all())
