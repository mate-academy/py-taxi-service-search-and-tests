from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import CarForm
from taxi.models import Manufacturer


class FormTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.driver1 = get_user_model().objects.create(
            username="driver1",
            license_number="DL001"
        )
        self.driver2 = get_user_model().objects.create(
            username="driver2",
            license_number="DL002"
        )

    def test_car_form_valid(self):
        form_data = {
            "model": "X5",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver1.id, self.driver2.id]
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
