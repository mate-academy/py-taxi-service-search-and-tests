from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.forms import DriverSearchForm, CarSearchForm, ManufacturerSearchForm
from taxi.models import Manufacturer, Car, Driver

DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class DriverSearchFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "bob"
        }
        Driver.objects.create(
            username="max",
            password="testPassword123",
            license_number="D2345670"
        )
        Driver.objects.create(
            username="serg",
            password="testPassword123",
            license_number="D3345670"
        )
        Driver.objects.create(
            username="jan",
            password="testPassword123",
            license_number="D4345670"
        )
        self.client.force_login(get_user_model().objects.create(
            username="bob",
            password="testPassword123"
        ))

    def test_valid_form(self):
        form = DriverSearchForm(self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_valid_char_field_kwargs(self):
        form = DriverSearchForm(self.form_data)
        username_field = form.fields["username"]

        self.assertEqual(username_field.max_length, 150)
        self.assertFalse(username_field.required)
        self.assertEqual(username_field.label, "")
        self.assertEqual(
            username_field.widget.attrs["placeholder"],
            "Search driver:"
        )

    def test_search_valid_results(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "max"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "max")
        self.assertNotContains(response, "serg")
        self.assertNotContains(response, "jan")

    def test_search_no_results(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "ksafas"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "serg")
        self.assertNotContains(response, "jan")

    def test_search_partial_match(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": "ma"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "max")
        self.assertNotContains(response, "serg")
        self.assertNotContains(response, "jan")

    def test_search_empty_query(self):
        response = self.client.get(DRIVER_LIST_URL, {"username": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "max")
        self.assertContains(response, "serg")
        self.assertContains(response, "jan")


class CarSearchFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "model": "bob"
        }
        manufacturer = Manufacturer.objects.create(name="test")
        Car.objects.create(model="Rs6", manufacturer=manufacturer)
        Car.objects.create(model="M3", manufacturer=manufacturer)
        Car.objects.create(model="Celica", manufacturer=manufacturer)
        self.client.force_login(get_user_model().objects.create(
            username="bob",
            password="testPassword123"
        ))

    def test_valid_form(self):
        form = CarSearchForm(self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_valid_char_field_kwargs(self):
        form = CarSearchForm(self.form_data)
        model_field = form.fields["model"]

        self.assertEqual(model_field.max_length, 150)
        self.assertFalse(model_field.required)
        self.assertEqual(model_field.label, "")
        self.assertEqual(
            model_field.widget.attrs["placeholder"],
            "Search car:"
        )

    def test_search_valid_results(self):
        response = self.client.get(CAR_LIST_URL, {"model": "Rs6"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rs6")
        self.assertNotContains(response, "M3")
        self.assertNotContains(response, "Celica")

    def test_search_no_results(self):
        response = self.client.get(CAR_LIST_URL, {"model": "bob"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Rs6")
        self.assertNotContains(response, "M3")
        self.assertNotContains(response, "Celica")

    def test_search_partial_match(self):
        response = self.client.get(CAR_LIST_URL, {"model": "Rs"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rs6")
        self.assertNotContains(response, "M3")
        self.assertNotContains(response, "Celica")

    def test_search_empty_query(self):
        response = self.client.get(CAR_LIST_URL, {"model": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rs6")
        self.assertContains(response, "M3")
        self.assertContains(response, "Celica")


class ManufacturerSearchFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "name": "bob"
        }
        Manufacturer.objects.create(name="Audi")
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Toyota")
        self.client.force_login(get_user_model().objects.create(
            username="bob",
            password="testPassword123"
        ))

    def test_valid_form(self):
        form = ManufacturerSearchForm(self.form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.form_data)

    def test_valid_char_field_kwargs(self):
        form = ManufacturerSearchForm(self.form_data)
        model_field = form.fields["name"]

        self.assertEqual(model_field.max_length, 150)
        self.assertFalse(model_field.required)
        self.assertEqual(model_field.label, "")
        self.assertEqual(
            model_field.widget.attrs["placeholder"],
            "Search manufacturer:"
        )

    def test_search_valid_results(self):
        response = self.client.get(
            MANUFACTURER_LIST_URL,
            {"name": "Audi"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Audi")
        self.assertNotContains(response, "BMW")
        self.assertNotContains(response, "Toyota")

    def test_search_no_results(self):
        response = self.client.get(
            DRIVER_LIST_URL,
            {"name": "bob"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Audi")
        self.assertNotContains(response, "BMW")
        self.assertNotContains(response, "Toyota")

    def test_search_partial_match(self):
        response = self.client.get(
            MANUFACTURER_LIST_URL,
            {"name": "BM"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Audi")
        self.assertNotContains(response, "Toyota")

    def test_search_empty_query(self):
        response = self.client.get(
            MANUFACTURER_LIST_URL,
            {"name": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Audi")
        self.assertContains(response, "BMW")
        self.assertContains(response, "Toyota")
