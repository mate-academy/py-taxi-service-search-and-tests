from django.test import TestCase

from taxi.forms import CarForm, CarSearchForm
from taxi.models import Manufacturer, Driver


class CarFormsTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="TestManufacturer", country="TestCountry"
        )
        self.driver1 = Driver.objects.create_user(
            username="driver1", password="testpass", license_number="ASD12345"
        )
        self.driver2 = Driver.objects.create_user(
            username="driver2", password="testpass", license_number="ASD67890"
        )

    def test_car_form_valid(self):
        data = {
            "model": "TestModel",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.driver1.pk, self.driver2.pk],
        }
        form = CarForm(data=data)
        self.assertTrue(form.is_valid())

    def test_car_form_save(self):
        data = {
            "model": "TestModel",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.driver1.pk, self.driver2.pk],
        }
        form = CarForm(data=data)
        if form.is_valid():
            car = form.save()
            self.assertEqual(car.model, data["model"])
            self.assertEqual(car.manufacturer, self.manufacturer)
            self.assertIn(self.driver1, car.drivers.all())
            self.assertIn(self.driver2, car.drivers.all())
        else:
            self.fail("This form invalid")

    def test_car_form_invalid(self):
        data = {
            "model": "",
            "manufacturer": self.manufacturer.pk,
        }
        form = CarForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("model", form.errors)

    def test_search_form_field_placeholder(self):
        form = CarSearchForm()
        self.assertEqual(
            form.fields["model"].widget.attrs["placeholder"],
            "model"
        )

    def test_search_form_model_field_max_length(self):
        form = CarSearchForm(data={"model": "a" * 256})
        self.assertFalse(form.is_valid())

    def test_search_form_model_field_required(self):
        form = CarSearchForm(data={"model": ""})
        self.assertFalse(form.is_valid())

    def test_search_form_model_field_valid_input(self):
        form = CarSearchForm(data={"model": "Toyota"})
        self.assertTrue(form.is_valid())
