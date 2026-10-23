from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Car


class ModelsTest(TestCase):
    def setUp(self):
        self.username = "test_driver"
        self.password = "secure_password123"
        self.driver = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
            first_name="test_name",
            last_name="test_name",
            license_number="ADM56983",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test_name", country="test_cnt"
        )

    def test_manufacturer_str(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}",
        )

    def test_driver_str(self):
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} {self.driver.last_name})",
        )

    def test_car_str(self):
        car = Car.objects.create(
            model="test_model", manufacturer=self.manufacturer
        )
        car.drivers.add(self.driver)
        self.assertEqual(str(car), "test_model")

    def test_driver_license_number(self):
        self.assertEqual(self.driver.username, "test_driver")
        self.assertEqual(self.driver.first_name, "test_name")
        self.assertEqual(self.driver.last_name, "test_name")
        self.assertEqual(self.driver.license_number, "ADM56983")

    def test_driver_abs_url(self):
        expected_url = reverse(
            "taxi:driver-detail", kwargs={"pk": self.driver.pk}
        )
        actual_url = self.driver.get_absolute_url()
        self.assertEqual(actual_url, expected_url)

    def test_get_absolute_url_resolves_correctly(self):
        self.client.login(username=self.username, password=self.password)
        url = self.driver.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class ListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="password123"
        )
        self.client.login(username="test_user", password="password123")

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.car = Car.objects.create(
            model="Mustang", manufacturer=self.manufacturer
        )
        self.driver = get_user_model().objects.create_user(
            username="schumacher", license_number="SHU11111"
        )

    def test_manufacturer_list_and_search(self):
        for i in range(5):
            Manufacturer.objects.create(name=f"Brand {i}", country="Test")

        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertIn("search_form", response.context)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

        # Перевірка фільтрації
        response = self.client.get(url, {"name": "toy"})
        self.assertEqual(len(response.context["manufacturer_list"]), 1)

    def test_car_list_and_search(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(url, {"model": "mus"})
        self.assertEqual(len(response.context["car_list"]), 1)

    def test_driver_list_and_search(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(url, {"username": "schu"})
        self.assertEqual(len(response.context["driver_list"]), 1)

    def test_login_required(self):
        self.client.logout()
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertRedirects(response, f"/accounts/login/?next={url}")


class ToggleAssignToCarTest(TestCase):
    def setUp(self):
        self.username = "driver_tester"
        self.password = "secure_pass123"
        self.user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
            license_number="XYZ12345",
        )
        self.client.login(username=self.username, password=self.password)

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.car = Car.objects.create(
            model="Camry", manufacturer=self.manufacturer
        )

        self.url = reverse(
            "taxi:toggle-car-assign", kwargs={"pk": self.car.pk}
        )
        self.expected_redirect = reverse(
            "taxi:car-detail", args=[self.car.pk]
        )

    def test_toggle_assign_to_car_behavior(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, self.expected_redirect)
        self.assertIn(self.car, self.user.cars.all())

        response = self.client.get(self.url)
        self.assertRedirects(response, self.expected_redirect)
        self.assertNotIn(self.car, self.user.cars.all())


class DriverFormsTest(TestCase):
    def test_driver_creation_form_is_valid(self):
        form_data = {
            "username": "new_driver",
            "password1": "dhG7!fks9_QaaX",
            "password2": "dhG7!fks9_QaaX",
            "license_number": "ABC12345",
            "first_name": "Oleg",
            "last_name": "Losos",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_is_valid(self):
        form_data = {"license_number": "XYZ98765"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_license_number_wrong_length(self):
        form_data = {"license_number": "AB1234"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_lowercase_letters(self):
        form_data = {"license_number": "abc12345"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)

    def test_license_number_not_digits_at_end(self):
        form_data = {"license_number": "ABC1234F"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("license_number", form.errors)
