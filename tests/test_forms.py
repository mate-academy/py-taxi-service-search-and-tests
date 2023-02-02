from django.test import TestCase

from taxi.forms import DriverSearchForm, DriverCreationForm
from taxi.models import Driver


class DriverSearchFormTest(TestCase):
    def setUp(self) -> None:
        self.user = Driver.objects.create_user(
            username="test_user",
            first_name="test",
            last_name="user",
            password="User12345"
        )

        self.client.login(username=self.user.username, password="User12345")

    def test_driver_creation_form_with_license_number_first_last_names_is_valid(self):
        form_data = {
            "username": "new_user1",
            "password1": "User1234test1",
            "password2": "User1234test1",
            "first_name": "Test first1",
            "last_name": "Test last1",
            "license_number": "TES12348"
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
