from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm
from taxi.models import Driver, Car, Manufacturer


class TestForms(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="testName",
            country="testTest"
        )
        self.car = Car.objects.create(
            model="Civic",
            manufacturer=self.manufacturer
        )
        self.driver = Driver.objects.create_user(
            username="testMan",
            password="test123"
        )

        self.client.login(username="testMan", password="test123")

    def test_license_number_form(self):
        form_data = {
            "license_number": "TES34238"
        }

        form = DriverLicenseUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
