from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

DRIVERS_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test user",
            password="test12345"
        )

    def test_login_required_drivers(self):
        response = self.client.get(DRIVERS_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_driver_detail_login_required(self):
        response = self.client.get(reverse(
            "taxi:driver-detail", kwargs={"pk": self.driver.id}
        ))

        self.assertNotEqual(response.status_code, 200)

    def test_driver_update_login_required(self):
        response = self.client.get(reverse(
            "taxi:driver-update", kwargs={"pk": self.driver.id}
        ))

        self.assertNotEqual(response.status_code, 200)

    def test_driver_create_login_required(self):
        response = self.client.get(reverse("taxi:driver-create"))

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test user",
            password="password456"
        )
        self.client.force_login(self.driver)

    def test_retrieve_drivers(self):
        for driver_id in range(2, 4):
            get_user_model().objects.create_user(
                username=f"driver{driver_id}",
                password=f"driver1234{driver_id}",
                license_number=f"RED1234{driver_id}"
            )

        response = self.client.get(DRIVERS_URL)

        drivers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_detail_login_required(self):
        response = self.client.get(reverse(
            "taxi:driver-detail", kwargs={"pk": self.driver.id}
        ))

        self.assertEqual(response.status_code, 200)

    def test_driver_create_login_required(self):
        response = self.client.get(reverse("taxi:driver-create"))

        self.assertEqual(response.status_code, 200)

    def test_driver_update_login_required(self):
        response = self.client.get(reverse(
            "taxi:driver-update", kwargs={"pk": self.driver.id}
        ))

        self.assertEqual(response.status_code, 200)

    def test_create_driver(self):
        form_data = {
            "username": "new_driver",
            "password1": "driver123test",
            "password2": "driver123test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "RED12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(
            new_driver.first_name,
            form_data["first_name"]
        )
        self.assertEqual(
            new_driver.last_name,
            form_data["last_name"]
        )
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"]
        )
        self.client.post(
            reverse("taxi:driver-create"),
            data=form_data
        )

    def test_search_driver_form(self):

        response = self.client.get(
            reverse("taxi:driver-detail",
                    kwargs={"pk": self.driver.id}
                    ) + "?username=test user"
        )

        self.assertContains(
            response,
            "test user"
        )
        self.assertNotContains(
            response,
            "Paul"
        )

    def test_get_absolute_url(self):
        driver = get_user_model().objects.get(id=1)

        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail",
                    kwargs={"pk": self.driver.id})
        )
