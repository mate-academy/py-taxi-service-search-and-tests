from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm, CarForm
from taxi.models import Car, Manufacturer


class FormsTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Toyota",
                                                        country="Japan")
        self.car = Car.objects.create(model="Corolla",
                                      manufacturer=self.manufacturer)

        self.driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="driver123",
            license_number="AGG11111",
        )
        self.driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="driver123",
            license_number="BGG11111",
        )
        self.driver3 = get_user_model().objects.create_user(
            username="driver3",
            password="driver123",
            license_number="CGG11111",
        )

    def test_driver_creation_form_with_username_password_license_number(
            self):
        form_data = {
            "username": "username",
            "password1": "Qwe123123",
            "password2": "Qwe123123",
            "first_name": "",
            "last_name": "",
            "license_number": "GGG11111",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_car_form_valid(self):
        form_data = {
            "model": "Camry",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id],
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        car = form.save()
        self.assertEqual(list(car.drivers.all()),
                         [self.driver1, self.driver2])
