from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver

DRIVERS_LIST_URL = reverse("taxi:driver-list")
PAGINATION = 5


class PublicDriverTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVERS_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="AAA54321",
            first_name="Admin",
            last_name="User",
            password="1qwerty2",
        )
        self.client.force_login(self.user)

        for i in range(0, PAGINATION + 1):
            Driver.objects.create(
                username=f"driver.user{i}",
                license_number=f"AAA1234{i}",
                first_name=f"Admin{i}",
                last_name=f"User{i}",
                password=f"1qwerty{i}",
            )

    def test_drivers_list(self):
        response = self.client.get(DRIVERS_LIST_URL)
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers[:PAGINATION]),
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_detail(self):
        response = self.client.get(reverse("taxi:driver-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_driver_list_response_with_correct_template(self):
        response = self.client.get(DRIVERS_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_detail_response_with_correct_template(self):
        response = self.client.get(reverse("taxi:driver-detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_update_driver_license_number_with_valid_data(self):
        test_license_number = "TES12345"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": test_license_number},
        )
        self.assertEqual(response.status_code, 302)

    def test_update_driver_license_number_with_not_valid_data(self):
        test_license_number = "1b"
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            data={"license_number": test_license_number},
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_driver(self):
        driver = get_user_model().objects.create(
            username="test-delete.user",
            license_number="TES53421",
            first_name="Test",
            last_name="Delete",
            password="1qwerty2",
        )
        response = self.client.post(
            reverse("taxi:driver-delete", kwargs={"pk": driver.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            get_user_model().objects.filter(id=driver.id).exists()
        )
