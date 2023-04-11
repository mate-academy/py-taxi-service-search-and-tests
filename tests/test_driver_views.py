from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVER_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Admin",
            password="test1234",
            license_number="AAA11111"
        )
        self.user2 = get_user_model().objects.create_user(
            username="Anton",
            password="test1234",
            license_number="QQQ11111"
        )
        self.user3 = get_user_model().objects.create_user(
            username="Sasha",
            password="test1234",
            license_number="SSS11111"
        )

        self.client.force_login(self.user)

    def test_driver_list(self) -> None:
        response = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_list_search(self) -> None:
        response = self.client.get(DRIVER_URL, {"username": "ant"})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertNotContains(response, "Sasha")
        self.assertContains(response, "Anton")

    def test_driver_detail(self) -> None:
        url = reverse("taxi:driver-detail", args=[self.user2.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")
        self.assertContains(response, self.user2.id)

    def test_driver_create(self) -> None:
        form_data = {
            "username": "new-user",
            "password1": "test1234GG",
            "password2": "test1234GG",
            "first_name": "First Name",
            "last_name": "Last Name",
            "license_number": "ASD11111"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(new_driver.license_number, form_data["license_number"])