from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.tests import fixtures


class DriverModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        fixtures.fill_db()

    def test_str(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_get_absolute_url_should_return_correct_url(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk}),
        )

    def test_license_number_field_max_length(self):
        driver = get_user_model().objects.get(id=1)
        max_length = driver._meta.get_field("license_number").max_length

        self.assertEqual(max_length, 255)

    def test_verbose_name(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(driver._meta.verbose_name, "driver")

    def test_verbose_name_plural(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(driver._meta.verbose_name_plural, "drivers")
