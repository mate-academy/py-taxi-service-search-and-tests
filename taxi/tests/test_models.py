from django.contrib.auth import get_user_model
from django.test import TestCase


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="test",
            password="Test123",
            first_name="Test_first",
            last_name="Test_last",
            license_number="ABC12345"
        )

    def test_str_method(self):
        driver = get_user_model().objects.get(id=1)
        expected_object_name = (f"{driver.username} "
                                f"({driver.first_name} "
                                f"{driver.last_name})")
        self.assertEqual(str(driver), expected_object_name)

    def test_driver_name_label(self):
        driver = get_user_model().objects.get(id=1)
        field_label = driver._meta.verbose_name
        self.assertEqual(field_label, "driver")

    def test_driver_name_label_plural(self):
        driver = get_user_model().objects.get(id=1)
        field_label = driver._meta.verbose_name_plural
        self.assertEqual(field_label, "drivers")

    def test_license_number_create(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(driver.license_number, "ABC12345")

    def test_license_number_name_label(self):
        driver = get_user_model().objects.get(id=1)
        field_label = driver._meta.get_field("license_number").verbose_name
        self.assertEqual(field_label, "license number")

    def test_license_number_max_length(self):
        driver = get_user_model().objects.get(id=1)
        max_length = driver._meta.get_field("license_number").max_length
        self.assertEqual(max_length, 255)

    def test_get_absolute_url(self):
        driver = get_user_model().objects.get(id=1)
        self.assertEqual(driver.get_absolute_url(), "/drivers/1/")
