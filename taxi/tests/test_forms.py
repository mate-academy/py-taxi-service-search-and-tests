from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import (
    DriverCreationForm,
    CarForm,
    CarSearchForm,
    ManufacturerSearchForm,
)
from taxi.models import Driver, Manufacturer, Car


class DriverFormTests(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="u1",
            password="pass",
            license_number="TST12345",
            first_name="<NAME>",
            last_name="<SURNAME>",
        )
        self.user2 = get_user_model().objects.create_user(
            username="u2",
            password="pass",
            license_number="TST54321",
            first_name="<NAME1>",
            last_name="<SURNAME1>",
        )

        self.client.force_login(self.user1)

    def test_driver_creation_form(self):
        form_data = {
            "username": "test_user",
            "password1": "<PASSWORD>",
            "password2": "<PASSWORD>",
            "license_number": "TST12345",
            "first_name": "<NAME>",
            "last_name": "<SURNAME>",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], form_data["username"])

    """
        Testing a search form in Django typically involves checking that:
        - The form renders correctly.
        - Submitting the form with valid input returns expected results.
        - Submitting with invalid or empty input behaves as expected
        (e.g. shows all results or none).
    """

    def test_driver_search_form_renders(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")
        self.assertContains(response, 'type="submit"')

    def test_search_returns_results(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "1"}
        )
        self.assertContains(response, self.user1.username)
        self.assertNotContains(response, self.user2.username)

    def test_search_empty_query_returns_all(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": ""}
        )
        self.assertContains(response, self.user1.username)
        self.assertContains(response, self.user2.username)


class CarFormTests(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="u1",
            password="pass",
            license_number="TST12345",
            first_name="<NAME>",
            last_name="<SURNAME>",
        )
        self.user2 = get_user_model().objects.create_user(
            username="u2",
            password="pass",
            license_number="TST54321",
            first_name="<NAME1>",
            last_name="<SURNAME1>",
        )
        self.client.force_login(self.user1)
        manufacturer = Manufacturer.objects.create(name="Tesla", country="USA")
        self.car1 = Car.objects.create(
            model="Model S", manufacturer=manufacturer
        )
        self.car2 = Car.objects.create(
            model="Model 3", manufacturer=manufacturer
        )
        self.car3 = Car.objects.create(
            model="Civic", manufacturer=manufacturer
        )

    def test_car_creation_form(self):
        manufacturer_form_data = {"name": "<NAME>", "country": "TEST_COUNTRY"}
        manufacturer = Manufacturer.objects.create(**manufacturer_form_data)
        car_form_data = {
            "model": "test_model",
            "manufacturer": manufacturer.id,
            "drivers": [self.user1.id, self.user2.id],
        }
        form = CarForm(data=car_form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["model"], car_form_data["model"])
        self.assertEqual(form.cleaned_data["manufacturer"], manufacturer)
        self.assertEqual(
            [driver.id for driver in form.cleaned_data["drivers"]],
            car_form_data["drivers"],
        )

    """
        Testing a search form in Django typically involves checking that:
        - The form renders correctly.
        - Submitting the form with valid input returns expected results.
        - Submitting with invalid or empty input behaves as expected
        (e.g. shows all results or none).
    """

    def test_car_search_form_renders(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["search_form"], CarSearchForm)
        self.assertContains(response, "<form")
        self.assertContains(response, 'type="submit"')

    def test_search_returns_results(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Model"}
        )
        self.assertEqual(response.status_code, 200)

        cars = response.context["car_list"]
        self.assertIn(self.car1, cars)
        self.assertIn(self.car2, cars)
        self.assertNotIn(self.car3, cars)

        self.assertContains(response, self.car1.model)
        self.assertContains(response, self.car2.model)
        self.assertNotContains(response, self.car3.model)

    def test_search_empty_query_returns_all(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": ""})
        self.assertContains(response, self.car1.model)
        self.assertContains(response, self.car2.model)
        self.assertContains(response, self.car3.model)


class ManufacturerFormTest(TestCase):
    def setUp(self):
        self.manufacturer1 = Manufacturer.objects.create(
            name="TEST_NAME", country="TEST_COUNTRY"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="TEST_NAME1", country="TEST_COUNTRY1"
        )

    def test_search_form_renders(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context["search_form"], ManufacturerSearchForm
        )
        self.assertContains(response, "<form")
        self.assertContains(response, 'type="submit"')

    def test_search_returns_results(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "name1"}
        )
        self.assertNotContains(response, self.manufacturer1.name)
        self.assertContains(response, self.manufacturer2.name)

    def test_search_empty_query_returns_all(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": ""})
        self.assertContains(response, self.manufacturer1.name)
        self.assertContains(response, self.manufacturer2.name)
