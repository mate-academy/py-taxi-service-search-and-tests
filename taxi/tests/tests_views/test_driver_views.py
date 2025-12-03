from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test_username",
            password="test123",
            license_number="ASD12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        get_user_model().objects.create_user(
            username="Test1",
            password="test123",
            license_number="ASD12346"
        )
        get_user_model().objects.create_user(
            username="Test2",
            password="test1223",
            license_number="ASD12347"
        )
        res = self.client.get(
            reverse("taxi:driver-list")
        )
        self.assertEqual(res.status_code, 200)
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(res.context["driver_list"]), list(drivers)
        )

    def test_search_driver_by_username(self):
        get_user_model().objects.create_user(
            username="Test1",
            password="test123",
            license_number="ASD12346"
        )
        get_user_model().objects.create_user(
            username="Test2",
            password="test1223",
            license_number="ASD12347"
        )
        res = self.client.get(
            reverse("taxi:driver-list"), data={"username": "Test1"}
        )
        self.assertContains(res, "Test1")
        self.assertNotContains(res, "Test2")


class CarChangeTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test_username",
            password="test123",
            license_number="ASD12345"
        )
        self.client.force_login(self.user)

    def test_driver_update_license_number_success_url(self):
        res = self.client.post(reverse(
            "taxi:driver-update", kwargs={"pk": self.user.pk}
        ), data={"license_number": self.user.license_number}
        )
        self.assertRedirects(res, reverse("taxi:driver-list"))

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ASS12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
