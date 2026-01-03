from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_URL = reverse("taxi:driver-list")
pagination_num = 5


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def create_users_for_test(self):
        get_user_model().objects.create_user(
            username="first_test_user",
            password="test123",
            license_number="AAA12345",
        )
        get_user_model().objects.create_user(
            username="second_test_user",
            password="test123",
            license_number="BBB12345",
        )
        for num in range(6):
            get_user_model().objects.create_user(
                username=f"{num}_test_user",
                password=f"{num}_test_pass",
                license_number=f"CCC{num}2345",
            )

    def test_retrieve_drivers(self):
        self.create_users_for_test()
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        users = list(Driver.objects.all())
        self.assertEqual(
            list(response.context["driver_list"]),
            list(users[:pagination_num])
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        search_response = self.client.get(f"{DRIVER_URL}?username=fir")
        self.assertContains(search_response, "first_test_user")
        self.assertNotContains(search_response, "second_test_user")

    def test_drivers_pagination(self):
        self.create_users_for_test()
        response = self.client.get(DRIVER_URL)
        self.assertEqual(len(response.context["driver_list"]), pagination_num)

    def test_driver_detail(self):
        self.create_users_for_test()
        driver = get_user_model().objects.get(id=1)
        response = self.client.get(
            reverse("taxi:driver-detail", args=[driver.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")
        self.assertEqual(response.context["user"], driver)
        self.assertContains(response, f"{driver.username}")
        self.assertContains(response, f"{driver.license_number}")
        response = self.client.get(reverse("taxi:driver-detail", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_create_driver(self):
        form_data = {
            "username": "test_username",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test First",
            "last_name": "Test Last",
            "license_number": "AAA12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
