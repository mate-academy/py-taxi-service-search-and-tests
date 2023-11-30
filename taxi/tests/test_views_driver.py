from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy

DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PublicDriverListViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200, )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertRedirects(response, "/accounts/login/?next=/drivers/")


class PrivateDriverListViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="TST12345",
        )
        self.client.force_login(self.user)

        number_of_drivers = 6
        for driver_num in range(number_of_drivers):
            get_user_model().objects.create_user(
                username=f"test user {driver_num}",
                password="password123",
                license_number=f"TST123{driver_num}",
            )

    def test_driver_list_view_url_exists_at_desired_location(self):
        response = self.client.get("/drivers/")
        self.assertEqual(response.status_code, 200)

    def test_driver_list_view_url_accessible_by_name(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_driver_list_view_uses_correct_template(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_list_pagination_is_five(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertTrue(len(response.context["driver_list"]) == 5)

    def test_driver_lists_all_drivers(self):
        response = self.client.get(DRIVER_LIST_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertTrue(len(response.context["driver_list"]) == 2)


class PrivateDriverCreateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="password123",
        )
        self.client.force_login(self.user)

    def test_create_driver(self):
        form_data = {
            "username": "test_username",
            "password1": "user12test",
            "password2": "user12test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TST12345",
        }
        self.client.post(DRIVER_CREATE_URL, data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class PrivateDriverUpdateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="TST12345",
        )
        self.client.force_login(self.user)

        self.data = {
            "license_number": "TST54321",
        }

    def test_update_drivers_licence_number(self):
        response = self.client.post(reverse(
            "taxi:driver-update", kwargs={"pk": self.user.id}),
            self.data
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.license_number, "TST54321")

    def test_view_drivers_licence_number_update_success_url(self):
        response = self.client.post(
            reverse("taxi:driver-update", kwargs={"pk": self.user.id}),
            self.data
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertRedirects(response, "/drivers/")
        self.assertRedirects(response, reverse_lazy("taxi:driver-list"))


class PrivateDriverDeleteViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="TST12345",
        )
        self.client.force_login(self.user)

        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            password="testDriver123",
            license_number="DRV11223",
        )

    def test_driver_delete_get_request(self):
        response = self.client.get(
            reverse("taxi:driver-delete", kwargs={"pk": self.driver.id})
        )
        self.assertContains(response, "Delete driver?")

    def test_driver_delete_post_request(self):
        post_response = self.client.post(
            reverse("taxi:driver-delete", kwargs={"pk": self.driver.id})
        )
        self.assertRedirects(
            post_response,
            reverse("taxi:driver-list"),
            status_code=302
        )
