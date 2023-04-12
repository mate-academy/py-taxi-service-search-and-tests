from django.test import TestCase
from taxi.models import Driver, Manufacturer
from taxi.forms import CarForm, DriverCreationForm, DriverLicenseUpdateForm


class TestCarForm(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer"
        )
        self.driver1 = Driver.objects.create_user(
            username="driver1",
            password="testpass123",
            license_number="ABC12345",
        )
        self.driver2 = Driver.objects.create_user(
            username="driver2",
            password="testpass123",
            license_number="ABD12345",
        )

        self.valid_data = {
            "model": "Test Model",
            "manufacturer": self.manufacturer.pk,
            "drivers": [self.driver1.pk, self.driver2.pk],
        }

    def test_car_form_valid(self):
        form = CarForm(data=self.valid_data)
        self.assertTrue(form.is_valid())


class DriverCreationFormTest(TestCase):
    def test_form_valid(self):
        data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
            "license_number": "ABC12345",
            "first_name": "Test",
            "last_name": "User",
        }
        form = DriverCreationForm(data=data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpassword"))
        self.assertIsInstance(user, Driver)
        self.assertEqual(user.license_number, "ABC12345")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")


class DriverLicenseUpdateFormTests(TestCase):
    test_cases = [
        {
            "name": "blank license number",
            "data": {"license_number": ""},
            "expected_error": ["This field is required."],
        },
        {
            "name": "invalid license number format",
            "data": {"license_number": "12345678"},
            "expected_error": [
                "First 3 characters should be uppercase letters"
            ],
        },
        {
            "name": "duplicate license number",
            "data": {},
            "driver1_data": {
                "username": "testuser1",
                "email": "testuser1@example.com",
                "license_number": "ABC12345",
            },
            "driver2_data": {
                "username": "testuser2",
                "email": "testuser2@example.com",
                "license_number": "ABC67890",
            },
            "expected_error": ["This field is required."],
        },
    ]

    def test_form_validation(self):
        for test_case in self.test_cases:
            with self.subTest(name=test_case["name"]):
                driver1 = Driver.objects.create(
                    username=test_case.get("driver1_data", {}).get(
                        "username", "testuser1"
                    ),
                    password="testpassword",
                    email=test_case.get("driver1_data", {}).get(
                        "email", "testuser1@example.com"
                    ),
                    license_number=test_case.get("driver1_data", {}).get(
                        "license_number", "ABC12345"
                    ),
                )
                driver2 = Driver.objects.create(
                    username=test_case.get("driver2_data", {}).get(
                        "username", "testuser2"
                    ),
                    password="testpassword",
                    email=test_case.get("driver2_data", {}).get(
                        "email", "testuser2@example.com"
                    ),
                    license_number=test_case.get("driver2_data", {}).get(
                        "license_number", "ABC67890"
                    ),
                )
                form = DriverLicenseUpdateForm(
                    instance=driver2, data=test_case.get("data", {})
                )
                self.assertFalse(form.is_valid())
                self.assertEqual(
                    form.errors["license_number"], test_case["expected_error"]
                )
                driver1.delete()
                driver2.delete()
