from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Driver, Car, Manufacturer


class SearchTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="test_123",
            license_number="EDA2232ASD8"
        )
        self.client.force_login(self.user)

    def test_driver_search(self):
        for i1 in range(4):
            for i in range(4):
                Driver.objects.create_user(
                    username=f"test{i1} user{i}",
                    password="test_123",
                    license_number=f"EDA{i1}2232ASD{i}",
                )
        responce = self.client.get(
            reverse("taxi:driver-list"), data={"username": "test2"}
        )
        self.assertEquals(
            list(responce.context_data.get("driver_list")),
            list(Driver.objects.filter(username__icontains="test2")),
        )

    def test_car_search(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Company", country="France"
        )
        for i in range(4):
            Car.objects.create(manufacturer=manufacturer, model=f"Test{i}")
        responce = self.client.get(
            reverse("taxi:car-list"),
            data={"model": "test"}
        )
        self.assertEquals(
            list(responce.context_data.get("car_list")),
            list(Car.objects.filter(model__icontains="test")),
        )

    def test_manufacturer_search(self):
        for i in range(4):
            Manufacturer.objects.create(name=f"Test{i}", country="France")
        responce = self.client.get(
            reverse("taxi:manufacturer-list"), data={"name": "test"}
        )
        self.assertEquals(
            list(responce.context_data.get("manufacturer_list")),
            list(Manufacturer.objects.filter(name__icontains="test")),
        )


class ModelMethodsTest(TestCase):

    def setUp(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="France"
        )
        Driver.objects.create_user(
            first_name="First",
            last_name="Second",
            username="test_user",
            password="test_123",
            license_number="EDA2232ASD",
        )
        Car.objects.create(manufacturer=manufacturer, model="Test_model")

    def test_str_models(self):
        self.assertEquals(str(Manufacturer.objects.first()), "Test France")
        self.assertEquals(str(Car.objects.first()), "Test_model")
        self.assertEquals(
            str(Driver.objects.first()),
            "test_user (First Second)"
        )

    def test_get_url_driver(self):
        driver = Driver.objects.first()
        self.assertEqual(driver.get_absolute_url(), f"/drivers/{driver.id}/")


class FormsTest(TestCase):

    def test_create_form_is_valid(self):
        form_data = {
            "license_number": "SWD13524",
            "username": "yAORS",
            "password1": "WEWQadf2SA@",
            "password2": "WEWQadf2SA@",
            "first_name": "Yaros",
            "last_name": "Biziuk",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_validator_form(self):
        form_data = {
            "license_number": "SWDw32dd",
            "first_name": "Yaros",
            "last_name": "Biziuk",
        }
        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form=form,
            field="license_number",
            errors="Last 5 characters should be digits",
        )
