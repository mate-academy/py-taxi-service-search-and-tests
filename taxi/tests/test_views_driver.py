from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicDriverTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="test_user_1",
            password="test password123",
            license_number="SDF12345"
        )

    def setUp(self) -> None:
        self.client = Client()

    def test_login_required_drivers(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/drivers/")

    def test_login_required_driver_detail(self):
        driver_detail = get_user_model().objects.get(pk=1)
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": driver_detail.pk})
        )
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/drivers/1/")

    def test_login_required_creation_driver_form(self):
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            "/accounts/login/?next=/drivers/create/"
        )


class PrivateDriverTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for user_id in range(8):
            get_user_model().objects.create_user(
                username=f"test_{user_id}",
                password="test password",
                license_number=f"QAY1234{user_id}"
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.get(pk=1)
        self.client.force_login(self.user)

    def test_drivers_pagination_is_five(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["driver_list"]), 5)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_pagination_second_page(self):
        response = self.client.get(DRIVER_LIST_URL + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["driver_list"]), 3)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_driver_detail(self):
        driver_detail = get_user_model().objects.get(pk=1)
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": driver_detail.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_create_driver(self):
        form_data = {
            "username": "test_user1",
            "first_name": "Test first",
            "last_name": "Test last",
            "password1": "Test password123",
            "password2": "Test password123",
            "license_number": "PAY56789",
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"]
        )

    def test_driver_search_result_matches_found(self):
        response = self.client.get("/drivers/?username=test_2")
        searching_driver = get_user_model().objects.filter(username="test_2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(searching_driver)
        )

    def test_driver_search_no_matches_found(self):
        response = self.client.get("/drivers/?username=Fake+name")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no drivers in the service.")

    def test_pagination_driver_search_with_value_current_page(self):
        response = self.client.get("/drivers/?username=Test")
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_pagination_driver_search_with_value_next_page(self):
        response = self.client.get("/drivers/?username=Test&page=2")
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["driver_list"]), 3)
