from django.test import TestCase
from django.contrib.auth import get_user_model
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    ManufacturerSearchForm,
    CarSearchForm,
    DriverSearchForm
)
from taxi.models import Car, Manufacturer


class FormsTestCase(TestCase):
    def setUp(self):
        self.manufacturer1 = Manufacturer.objects.create(
            name="Manufacturer One"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Manufacturer Two"
        )

        self.car1 = Car.objects.create(
            model="Model One",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Model Two",
            manufacturer=self.manufacturer2
        )

        self.driver1 = get_user_model().objects.create_user(
            username="driver_one",
            password="password123",
            license_number="AAA11111"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver_two",
            password="password123",
            license_number="BBB22222"
        )

    def test_car_form_valid(self):
        form_data = {
            "model": self.car1.model,
            "manufacturer": self.manufacturer1.pk,
            "drivers": [self.driver1.pk],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "newdriver",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "license_number": "CCC33333",
            "first_name": "Jane",
            "last_name": "Smith"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_valid(self):
        form_data = {"license_number": "ZZZ99999"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form(self):
        form = ManufacturerSearchForm(data={"name": "Manufacturer"})
        self.assertTrue(form.is_valid())
        results = Manufacturer.objects.filter(
            name__icontains=form.cleaned_data["name"]
        )
        self.assertIn(self.manufacturer1, results)
        self.assertIn(self.manufacturer2, results)

    def test_car_search_form(self):
        form = CarSearchForm(
            data={"model": "Model One"}
        )
        self.assertTrue(form.is_valid())
        results = Car.objects.filter(
            model__icontains=form.cleaned_data["model"]
        )
        self.assertIn(self.car1, results)
        self.assertNotIn(self.car2, results)

    def test_driver_search_form(self):
        form = DriverSearchForm(data={"username": "driver_one"})
        self.assertTrue(form.is_valid())
        results = get_user_model().objects.filter(
            username__icontains=form.cleaned_data["username"]
        )
        self.assertIn(self.driver1, results)
        self.assertNotIn(self.driver2, results)
