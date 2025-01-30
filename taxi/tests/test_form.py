from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm


class FormTest(TestCase):
    def test_driver_creation_form(self):
        form_data = {
            "username": "TestDriver",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.assertEqual(form.cleaned_data, form_data)
        response = self.client.post(
            reverse("taxi:driver-create"),
            data=form_data
        )
        self.assertEqual(response.status_code, 302)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(
            new_driver.username,
            form_data["username"]
        )
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"]
        )
        self.assertEqual(
            new_driver.first_name,
            form_data["first_name"]
        )
        self.assertTrue(
            new_driver.check_password(form_data["password1"])
        )

    def test_driver_validate_password(self):
        form_data1 = {
            "username": "TestDriver1",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "ABC1234"
        }
        form1 = DriverCreationForm(data=form_data1)
        self.assertFalse(form1.is_valid())
        self.assertIn("license_number", form1.errors)

        form_data2 = {
            "username": "TestDriver2",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "AB012345"
        }
        form2 = DriverCreationForm(data=form_data2)
        self.assertFalse(form2.is_valid())
        self.assertIn("license_number", form2.errors)

        form_data3 = {
            "username": "TestDriver3",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "ABc12345"
        }
        form3 = DriverCreationForm(data=form_data3)
        self.assertFalse(form3.is_valid())
        self.assertIn("license_number", form3.errors)

        form_data4 = {
            "username": "TestDriver4",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "first_name": "First",
            "last_name": "Last",
            "license_number": "ABc1234"
        }
        form4 = DriverCreationForm(data=form_data4)
        self.assertFalse(form4.is_valid())
        self.assertIn("license_number", form4.errors)

    def test_license_number_update(self):
        driver = get_user_model().objects.create_user(
            username="TestDriver",
            password="password123",
            license_number="ABC12345"
        )
        form_data = {
            "license_number": "XYZ98765",
        }

        form = DriverLicenseUpdateForm(data=form_data, instance=driver)
        self.assertTrue(form.is_valid(), form.errors)
        updated_driver = form.save()
        # Перевіряємо, що номер посвідчення оновився
        self.assertEqual(updated_driver.license_number, "XYZ98765")
