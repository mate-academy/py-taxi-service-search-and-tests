from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm, CarForm
from taxi.models import Driver, Manufacturer


class FormsTests(TestCase):
    def test_driver_creation_form_with_license_number(self) -> None:
        form_data = {
            "username": "new_user",
            "first_name": "Test Name",
            "last_name": "Test Last",
            "password1": "HardPassword12345",
            "password2": "HardPassword12345",
            "license_number": "ABC12345",
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_valid_license_update(self) -> None:

        driver = get_user_model().objects.create_user(
            username="driver1",
            password="HardPassword12345",
            license_number="ABC12345"
        )

        form_data = {
            "license_number": "XYZ12345",
        }
        form = DriverLicenseUpdateForm(data=form_data, instance=driver)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["license_number"], "XYZ12345")

    def test_valid_car_form(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Testland"
        )
        driver1 = get_user_model().objects.create_user(
            username="driver1",
            password="pass1pass1",
            license_number="ABC12345"
        )
        driver2 = get_user_model().objects.create_user(
            username="driver2",
            password="pass1pass1",
            license_number="XYZ12345"
        )

        form_data = {
            "model": "Test Car",
            "manufacturer": manufacturer.id,
            "drivers": [driver1.id, driver2.id]
        }
        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
        car = form.save()

        self.assertEqual(list(car.drivers.all()), [driver1, driver2])
