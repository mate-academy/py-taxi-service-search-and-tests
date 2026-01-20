from django.contrib.auth import get_user_model
from django.test import TestCase
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
    DriverSearchForm,
    CarSearchForm,
    ManufacturerSearchForm,
)
from taxi.models import Manufacturer


class TestCarForm(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username="user1", password="password1", license_number="ABC12345"
        )
        self.user2 = get_user_model().objects.create_user(
            username="user2", password="password2", license_number="ADC12345"
        )

        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

    def test_valid_form(self):
        data = {
            "model": "Test Model",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.user1.pk, self.user2.pk],
        }
        form = CarForm(data=data)
        self.assertTrue(form.is_valid(), form.errors)
