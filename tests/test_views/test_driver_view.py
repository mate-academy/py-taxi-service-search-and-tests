from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


DRIVERS_LIST_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="test12345"
        )

    def test_driver_list_login_required(self):
        res = self.client.get(DRIVERS_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_driver_detail_login_required(self):
        res = self.client.get(reverse(
            "taxi:driver-detail", args=[self.driver.id]
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_driver_update_login_required(self):
        res = self.client.get(reverse(
            "taxi:driver-update", args=[self.driver.id]
        ))
        self.assertNotEqual(res.status_code, 200)

    def test_driver_create_login_required(self):
        res = self.client.get(reverse("taxi:driver-create"))
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="test12345"
        )
        self.client.force_login(self.driver)

    def test_driver_list_login_required(self):
        res = self.client.get(DRIVERS_LIST_URL)
        self.assertEqual(res.status_code, 200)

    def test_driver_detail_login_required(self):
        res = self.client.get(reverse(
            "taxi:driver-detail", args=[self.driver.id]
        ))
        self.assertEqual(res.status_code, 200)

    def test_driver_update_login_required(self):
        res = self.client.get(reverse(
            "taxi:driver-update", args=[self.driver.id]
        ))
        self.assertEqual(res.status_code, 200)

    def test_driver_create_login_required(self):
        res = self.client.get(reverse("taxi:driver-create"))
        self.assertEqual(res.status_code, 200)

    def test_search_by_username_in_driver_list(self):
        for num in range(3):
            get_user_model().objects.create_user(
                username=f"driver{num}",
                password="user12345",
                license_number=f"AAA1111{num}"
            )
        search_word = "driver2"
        response = self.client.get(f"{DRIVERS_LIST_URL}?field={search_word}")
        searched_query = get_user_model().objects.filter(
            username__icontains=search_word
        )
        self.assertQuerysetEqual(
            response.context["driver_list"], searched_query
        )

    def test_create_driver(self):
        form_data = {
            "username": "test",
            "password1": "test12345",
            "password2": "test12345",
            "first_name": "Test",
            "last_name": "User",
            "license_number": "ESS12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
