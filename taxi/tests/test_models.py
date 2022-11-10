from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelsTests(TestCase):
    def test_driver_str(self):
        driver_ = get_user_model().objects.create_user(
            username="test",
            password="test12345",
            first_name="Test first",
            last_name="Test last"
        )

        self.assertEqual(
            str(driver_),
            f"{driver_.username} ({driver_.first_name} {driver_.last_name})")
