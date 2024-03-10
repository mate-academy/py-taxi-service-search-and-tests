from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import CarForm

from taxi.models import Manufacturer


class CarFormTest(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Honda",
            country="USA"
        )
        self.driver = get_user_model().objects.create_user(
            username="krixn",
            first_name="Serhii",
            last_name="Haiduchyk",
            password="1337"
        )

    def test_car_creation_form(self) -> None:
        form_data = {
            "model": "Honda",
            "manufacturer": self.manufacturer,
            "drivers": get_user_model().objects.all()
        }

        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
