from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from taxi.forms import DriverLicenseUpdateForm, DriverCreationForm
from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="VAG",
            country="Germany"
        )
        self.assertEqual(str(manufacturer),
                         f"{manufacturer.name} {manufacturer.country}"
                         )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="VAG",
            country="Germany"
        )
        car = Car.objects.create(model="test", manufacturer=manufacturer)
        self.assertEqual(str(car), car.model)

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last"
        )
        self.assertEqual(str(driver),
                         f"{driver.username}"
                         f" ({driver.first_name} {driver.last_name})"
                         )

    def test_create_driver_with_license_number(self):
        username = "test"
        password = "test12345"
        license_number = "LOL12345"
        driver = get_user_model().objects.create_user(
            username=username,
            password=password,
            license_number=license_number
        )
        self.assertEqual(driver.username, username)
        self.assertTrue(driver.check_password(password))
        self.assertEqual(driver.license_number, license_number)

    def test_driver_license_update_form_with_invalid_license_number(self):
        form_data = {"license_number": "12345LOL"}
        form = DriverLicenseUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
