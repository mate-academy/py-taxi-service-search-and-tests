import pytest

from taxi.forms import DriverLicenseUpdateForm


class TestDriverForms:
    @pytest.mark.django_db
    @pytest.mark.parametrize(
        "number, expected_result",
        [
            pytest.param(
                "ABC12345",
                True,
                id="'ABC12345' should pass license number validation",
            ),
            pytest.param(
                "ABC1234",
                False,
                id="'ABC1234' shouldn't pass license number validation: "
                "too short",
            ),
            pytest.param(
                "ABC123456",
                False,
                id="'ABC123456' shouldn't pass license number validation: "
                "too long",
            ),
            pytest.param(
                "ABCA2345",
                False,
                id="'ABCA2345' shouldn't pass license number validation: "
                "incorrect number of letters and digits",
            ),
            pytest.param(
                "abc12345",
                False,
                id="'abc12345' shouldn't pass license number validation: "
                "lowercase letters",
            ),
            pytest.param(
                "12345ABC",
                False,
                id="'12345ABC' shouldn't pass license number validation: "
                "incorrect order",
            ),
        ],
    )
    def test_license_number_validation(self, number, expected_result):
        form_data = {"license_number": number}

        form = DriverLicenseUpdateForm(data=form_data)

        assert form.is_valid() == expected_result
