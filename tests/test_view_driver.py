from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicDriverListTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertNotEquals(response.status_code, 200)
        self.assertRedirects(
            response,
            "/accounts/login/?next=/drivers/"
        )


class PrivateDriverListTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for driver_id in range(8):
            get_user_model().objects.create_user(
                username=f"test_user_{driver_id}",
                password="1testpassword2",
                license_number=f"TES1234{driver_id}"
            )

    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test_user",
            password="1qazcde3",
        )
        self.client.force_login(self.driver)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/drivers/")

        self.assertEquals(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/driver_list.html"
        )


class PrivateDriverCreateTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test_user",
            password="1qazcde3",
        )
        self.client.force_login(self.driver)

    def test_create_driver(self):
        form_data = {
            "username": "test_user_create",
            "password1": "test_password_12345",
            "password2": "test_password_12345",
            "first_name": "Test First",
            "last_name": "Test Last",
            "license_number": "CRE12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEquals(new_driver.first_name, form_data["first_name"])
        self.assertEquals(new_driver.last_name, form_data["last_name"])
        self.assertEquals(
            new_driver.license_number,
            form_data["license_number"]
        )
