from django.test import TestCase
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer


class ModelsTests(TestCase):
    def test_driver_str(self) -> None:
        test_driver = get_user_model().objects.create_user(
            username="test.user",
            email="test@test.com",
            first_name="TestFirst",
            last_name="TestLast",
            password="testpassword123",
        )
        username = test_driver.username
        first_name = test_driver.first_name
        last_name = test_driver.last_name
        self.assertEqual(
            str(test_driver),
            f"{username} ({first_name} {last_name})"
        )

    def test_manufacturer_str(self) -> None:
        test_manufacturer = Manufacturer.objects.create(
            name="TestName",
            country="TestCountry",
        )
        self.assertEqual(
            str(test_manufacturer),
            f"{test_manufacturer.name} {test_manufacturer.country}"
        )
