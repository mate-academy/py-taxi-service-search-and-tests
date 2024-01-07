import pytest
from taxi.forms import DriverCreationForm


@pytest.mark.django_db
class TestForm:
    form_data = {
        "username": "TestUser",
        "password1": "testPass1",
        "password2": "testPass1",
        "first_name": "Test Firstname",
        "last_name": "Test Lastname",
    }

    def test_valid_license_number(self):
        form_data = {**self.form_data, "license_number": "ABC12345"}
        form = DriverCreationForm(data=form_data)
        assert form.is_valid()

    @pytest.mark.parametrize(
        "license_number, is_valid",
        [
            ("A", False),
            ("1", False),
            ("12345", False),
            ("QWERTYUI", False),
            ("12345678", False),
            ("abc12345", False),
        ]
    )
    def test_invalid_license_number(self, license_number, is_valid):
        form_data = {**self.form_data, "license_number": license_number}
        form = DriverCreationForm(data=form_data)
        assert form.is_valid() is is_valid
