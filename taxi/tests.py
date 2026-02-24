from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.forms import (
    DriverCreationForm,
    DriversSearchForm,
    CarsSearchForm,
    ManufacturersSearchForm
)
from taxi.models import Manufacturer, Car


class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="test_n",
            country="test_c"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_driver_url(self):
        driver = get_user_model().objects.create_user(
            username="test_driver",
            password="test123",
            license_number="test_license_number",
        )
        self.assertEqual(
            driver.get_absolute_url(),
            f"/drivers/{driver.pk}/"
        )


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="test1234"
        )
        self.client.force_login(self.admin_user)
        self.manufacturer = Manufacturer.objects.create(
            name="test_n",
            country="test_c",
        )

    def test_manufacturer_listed(self):
        """
        Test that the manufacturer is in the list ig
        """
        url = reverse("admin:taxi_manufacturer_changelist")
        result = self.client.get(url)
        self.assertContains(
            result,
            self.manufacturer.country,
        )


class PublicViewsTests(TestCase):
    def test_login_required(self):
        url = reverse("taxi:driver-list")
        result = self.client.get(url)
        self.assertNotEqual(
            result.status_code,
            200
        )


class LoggedInViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test1234",
            license_number="test_license_number",
        )
        self.client.force_login(self.user)

    def test_manufacturer_list_len(self):
        Manufacturer.objects.create(name="test_2", country="test_c")
        Manufacturer.objects.create(name="test_1", country="test_c")
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(len(manufacturers), 2)

    def test_correct_template(self):
        response = self.client.get(
            reverse(
                "taxi:manufacturer-list",
            )
        )
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )


class FormsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test1234",
            license_number="test_license_number",
        )
        self.client.force_login(self.user)

        self.manufacturer = Manufacturer.objects.create(
            name="search_name",
            country="test_c",
        )

        self.car = Car.objects.create(
            model="search_model",
            manufacturer=self.manufacturer,
        )


    def test_driver_creation(self):
        form_data = {
            "username": "test_driver",
            "license_number": "ABC66767",
            "password1": "1qazcde3",
            "password2": "1qazcde3",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        }
        form = DriverCreationForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_search_driver(self):
        form_data = {
            "username": "test_user",
        }
        form = DriversSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "test_user"}
        )
        self.assertContains(
            response,
            self.user.username,
        )

    def test_cars_search(self):
        form_data = {
            "model": "search_model",
        }
        form = CarsSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "search_model"}
        )
        self.assertContains(
            response,
            self.car.model,
        )

    def test_manufacturers_search(self):
        form_data = {
            "name": "search_name",
        }
        form = ManufacturersSearchForm(data=form_data)

        self.assertTrue(form.is_valid())

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "search_name"}
        )
        self.assertContains(
            response,
            self.manufacturer.name,
        )
