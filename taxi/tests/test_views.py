from django.test import TestCase
from django.contrib.auth import get_user_model


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user1",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_creation_user(self):
        self.assertEqual(self.user.username, "user1")

    def test_validation_password(self):
        self.assertTrue(self.user.check_password("test123"))
