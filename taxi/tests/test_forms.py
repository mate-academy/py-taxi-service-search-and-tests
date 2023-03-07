from django.test import TestCase

from taxi.forms import DriverCreationForm, CommentForm


class FormsTests(TestCase):
    def test_driver_creation_form_with_additional_info_is_valid(self):
        """Test that driver creates with first_name,
        last_name and license_number"""
        form_data = {
            "username": "user_test",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "test",
            "last_name": "test",
            "license_number": "ABC12345",
            "avatar": None,
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_comment_creation_form_data_is_valid(self):
        form_data = {"content": "Test comment!"}
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
