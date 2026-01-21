from django.test import TestCase
from django.contrib.admin.sites import site
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Driver, Car, Manufacturer
from taxi.forms import DriverSearchForm, CarSearchForm, ManufacturerSearchForm
from taxi.admin import DriverAdmin, CarAdmin


class AdminTests(TestCase):
    def test_driver_admin_registered(self):
        self.assertIn(Driver, site._registry)
        self.assertIsInstance(site._registry[Driver], DriverAdmin)

    def test_car_admin_registered(self):
        self.assertIn(Car, site._registry)
        self.assertIsInstance(site._registry[Car], CarAdmin)

    def test_manufacturer_admin_registered(self):
        self.assertIn(Manufacturer, site._registry)


class ModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.driver = Driver.objects.create_user(
            username="driver1",
            password="pass",
            first_name="Test",
            last_name="Driver",
            license_number="ABC123",
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.driver)

    def test_driver_str(self):
        self.assertEqual(str(self.driver), "driver1 (Test Driver)")

    def test_car_str(self):
        self.assertEqual(str(self.car), "Corolla")

    def test_manufacturer_str(self):
        self.assertEqual(str(self.manufacturer), "Toyota Japan")

    def test_get_absolute_url(self):
        url = self.driver.get_absolute_url()
        self.assertEqual(
            url,
            reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk})
        )


class SearchFormsTest(TestCase):
    def test_driver_search_form_valid_data(self):
        form = DriverSearchForm(data={"username": "testdriver"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testdriver")

    def test_driver_search_form_empty_data(self):
        form = DriverSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_car_search_form_valid_data(self):
        form = CarSearchForm(data={"model": "Toyota"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "Toyota")

    def test_car_search_form_empty_data(self):
        form = CarSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], "")

    def test_manufacturer_search_form_valid_data(self):
        form = ManufacturerSearchForm(data={"name": "Ford"})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Ford")

    def test_manufacturer_search_form_empty_data(self):
        form = ManufacturerSearchForm(data={})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_fields_present(self):
        self.assertIn("username", DriverSearchForm().fields)
        self.assertIn("model", CarSearchForm().fields)
        self.assertIn("name", ManufacturerSearchForm().fields)


class ViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.login(username="testuser", password="testpass")
        Manufacturer.objects.create(name="Ford", country="USA")

    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")
        self.assertIn("num_drivers", response.context)

    def test_manufacturer_list_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ford")
