from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import CarForm, DriverLicenseUpdateForm
from taxi.models import Manufacturer, Driver, Car


class ModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="manufacturer",
            country="country"
        )
        self.driver = get_user_model().objects.create(
            username="driver",
            password="password",
            license_number="license_number"
        )
        self.car = Car.objects.create(
            model="model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_string(self):
        self.assertEqual(
            str(self.manufacturer),
            f"{self.manufacturer.name} {self.manufacturer.country}"
        )
        self.assertEqual(
            str(self.driver),
            f"{self.driver.username} "
            f"({self.driver.first_name} "
            f"{self.driver.last_name})"
        )
        self.assertEqual(
            str(self.car),
            self.car.model
        )

    def test_car_delete(self):
        self.manufacturer.delete()
        self.assertEqual(
            list(Car.objects.filter(manufacturer__name="manufacturer")),
            []
        )


class TestAdminRequired(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin"
        )

    def test_without_login(self):
        url = reverse("taxi:index")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 302)

    def test_with_login(self):
        self.client.force_login(self.admin_user)
        url = reverse("taxi:index")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)


class TestViews(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin"
        )
        self.client = Client()
        self.manufacturer = Manufacturer.objects.create(
            name="manufacturer",
            country="country"
        )

    def test_view_index_count(self) -> None:
        self.client.force_login(self.admin_user)
        url = reverse("taxi:index")
        res = self.client.get(url)
        self.assertEqual(res.context["num_drivers"], 1)
        self.assertEqual(res.context["num_cars"], 0)
        self.assertEqual(res.context["num_manufacturers"], 1)


class FormTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_superuser(
            username="admin",
            password="admin"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="manufacturer",
            country="country"
        )
        self.car = Car.objects.create(
            model="model",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_car_form_is_valid(self):
        form_data = {
            "model": "test",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id]
        }
        form = CarForm(data=form_data)
        self.assertEqual(form.is_valid(), True)

    def test_car_form_is_not_valid(self):
        form_data = {
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id]
        }
        form = CarForm(data=form_data)
        self.assertEqual(form.is_valid(), False)

        form_data = {
            "model": "test",
            "drivers": [self.driver.id]
        }
        form = CarForm(data=form_data)
        self.assertEqual(form.is_valid(), False)

        form_data = {
            "model": "test",
            "manufacturer": self.manufacturer.id,
        }
        form = CarForm(data=form_data)
        self.assertEqual(form.is_valid(), False)

        form_data = {
            "model": "test",
            "manufacturer": self.manufacturer.id,
            "drivers": self.driver.id
        }
        form = CarForm(data=form_data)
        self.assertEqual(form.is_valid(), False)

    def test_driver_license_update_form(self):
        form_data = {
            "license_number": "ABC12345"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertEqual(form.is_valid(), True)

        form_data = {
            "license_number": "ABC1234"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertEqual(form.is_valid(), False)

        form_data = {
            "license_number": "ABb12345"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertEqual(form.is_valid(), False)

        form_data = {
            "license_number": "ABCa2345"
        }
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertEqual(form.is_valid(), False)
