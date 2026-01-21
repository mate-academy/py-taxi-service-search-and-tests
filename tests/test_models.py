from django.test import TestCase

from taxi.models import Driver


class ModelTests(TestCase):
    def setUp(self) -> None:
        Driver.objects.create(
            license_number="ACB1234",
            username="Vasaik",
            first_name="Vasyl",
            last_name="Valish"
        )

    def test_verbose_name(self):
        verbose_name = Driver._meta.verbose_name
        self.assertEqual(verbose_name, "driver")

    def test_verbose_name_plural(self):
        verbose_name_plural = Driver._meta.verbose_name_plural
        self.assertEqual(verbose_name_plural, "drivers")

    def test_str(self):
        driver = Driver.objects.get(id=1)
        value_check = (f"{driver.username} "
                       f"({driver.first_name} {driver.last_name})")
        self.assertEqual(str(driver), value_check)
