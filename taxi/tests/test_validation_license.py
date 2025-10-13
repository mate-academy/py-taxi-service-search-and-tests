from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class TestValidationDriverLicense(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="testuser",
            password="test1234"
        )
        self.client.force_login(user)

    def test_validation_with_correct_data(self):
        user = get_user_model().objects.get(username="testuser")
        data = {"license_number" : "TES12345"}
        url = reverse("taxi:driver-update", args=[user.id])
        self.client.post(url, data=data)
        new_user = get_user_model().objects.get(username="testuser")
        self.assertEqual(new_user.license_number, "TES12345")

    def test_validation_with_too_long_data(self):
        user = get_user_model().objects.get(username="testuser")
        data = {"license_number" : "TES123456"}
        url = reverse("taxi:driver-update", args=[user.id])
        self.client.post(url, data=data)
        new_user = get_user_model().objects.get(username="testuser")
        self.assertEqual(new_user.license_number, "")

    def test_validation_with_lower_data(self):
        user = get_user_model().objects.get(username="testuser")
        data = {"license_number" : "tes12345"}
        url = reverse("taxi:driver-update", args=[user.id])
        self.client.post(url, data=data)
        new_user = get_user_model().objects.get(username="testuser")
        self.assertEqual(new_user.license_number, "")

    def test_validation_with_only_letter_data(self):
        user = get_user_model().objects.get(username="testuser")
        data = {"license_number" : "TESTTEST"}
        url = reverse("taxi:driver-update", args=[user.id])
        self.client.post(url, data=data)
        new_user = get_user_model().objects.get(username="testuser")
        self.assertEqual(new_user.license_number, "")

    def test_validation_with_short_data(self):
        user = get_user_model().objects.get(username="testuser")
        data = {"license_number" : "TES1234"}
        url = reverse("taxi:driver-update", args=[user.id])
        self.client.post(url, data=data)
        new_user = get_user_model().objects.get(username="testuser")
        self.assertEqual(new_user.license_number, "")
