from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.forms import CarForm
from taxi.models import Manufacturer


class CarFormTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="password1",
            license_number="AAA12345"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="password2",
            license_number="BBB12345"
        )
        self.driver3 = get_user_model().objects.create_user(
            username="driver3",
            password="password3",
            license_number="CCC12345"
        )

    def test_car_form_valid_data(self):
        form_data = {
            "model": "Camry",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_form_invalid_data(self):
        form_data = {
            "model": "",  # Empty value, which should be invalid
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver3.id],
        }
        form = CarForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_car_form_save(self):
        form_data = {
            "model": "Mustang",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver2.id, self.driver3.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())

        car = form.save()

        self.assertEqual(car.model, "Mustang")
        self.assertEqual(car.manufacturer, self.manufacturer)
        self.assertListEqual(
            list(car.drivers.all()), [self.driver2, self.driver3]
        )
