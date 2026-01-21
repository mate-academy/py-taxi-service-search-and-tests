from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


Driver = get_user_model()


class DriverListViewTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="test_user",
            password="test123",
        )
        self.client.force_login(self.user)
        self.url = reverse("taxi:driver-list")

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=" + self.url)

    def test_context_contains_search_form(self):
        response = self.client.get(self.url + "?username=test")
        self.assertIn("search_form", response.context)
        form = response.context["search_form"]
        self.assertEqual(form.initial.get("username"), "test")

    def test_search_partial_match(self):
        Driver.objects.create_user(
            username="test1",
            password="test123",
            license_number="TST12345"
        )
        Driver.objects.create_user(
            username="test2",
            password="test123",
            license_number="TST54321"
        )

        response = self.client.get(self.url + "?username=test1")
        driver_usernames = [
            driver.username for driver in response.context["driver_list"]
        ]
        self.assertIn("test1", driver_usernames)
        self.assertNotIn("test2", driver_usernames)

    def test_search_empty(self):
        Driver.objects.create_user(
            username="test1",
            password="test123",
            license_number="TST12345"
        )
        Driver.objects.create_user(
            username="test2", password="test123", license_number="TST54321"
        )

        response = self.client.get(self.url)
        driver_usernames = [
            driver.username for driver in response.context["driver_list"]
        ]
        self.assertIn("test1", driver_usernames)
        self.assertIn("test2", driver_usernames)

    def test_pagination(self):
        for i in range(9):
            Driver.objects.create_user(
                username=f"test{i}",
                password="test123",
                license_number=f"TST1234{i}"
            )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_pagination_with_search(self):

        for i in range(8):
            Driver.objects.create_user(
                username=f"test{i}",
                password="test123",
                license_number=f"TST1234{i}"
            )

        response = self.client.get(self.url + "?username=test&page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 4)


class DriverCreateViewTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="test_user",
            password="test123",
        )
        self.client.force_login(self.user)
        self.url = reverse("taxi:driver-create")

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=" + self.url)

    def test_status_code_200_and_uses_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "taxi/driver_form.html")
        self.assertEqual(response.status_code, 200)

    def test_create_driver(self):
        data = {
            "username": "test",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "TST12345",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(Driver.objects.count(), 2)
        self.assertRedirects(
            response,
            reverse(
                "taxi:driver-detail", kwargs={"pk": 2}
            )
        )

    def test_create_driver_invalid(self):
        data = {
            "username": "",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "license_number": "TST12345",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(Driver.objects.count(), 1)
        self.assertFormError(
            response.context["form"], "username", "This field is required."
        )


class DriverUpdateLicenseViewTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="test_user",
            password="test123",
        )
        self.client.force_login(self.user)
        self.driver = Driver.objects.create_user(
            username="test", password="test123", license_number="TST12345"
        )
        self.url = reverse("taxi:driver-update", kwargs={"pk": self.driver.pk})

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=" + self.url)

    def test_status_code_200_and_uses_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "taxi/driver_form.html")
        self.assertEqual(response.status_code, 200)

    def test_update_driver_license(self):
        data = {
            "license_number": "TST54321",
        }
        old_driver_license = self.driver.license_number
        response = self.client.post(self.url, data)
        self.driver.refresh_from_db()
        self.assertNotEqual(self.driver.license_number, old_driver_license)
        self.assertRedirects(response, reverse("taxi:driver-list"))

    def test_update_driver_license_invalid(self):
        data = {
            "license_number": "12345TST54321",
        }
        old_driver_license = self.driver.license_number
        response = self.client.post(self.url, data)
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.license_number, old_driver_license)
        self.assertFormError(
            response.context["form"],
            "license_number",
            "License number should consist of 8 characters",
        )


class DriverDeleteViewTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="test_user",
            password="test123",
        )
        self.client.force_login(self.user)
        self.driver = Driver.objects.create_user(
            username="test", password="test123", license_number="TST12345"
        )
        self.url = reverse("taxi:driver-delete", kwargs={"pk": self.driver.id})

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login") + "?next=" + self.url)

    def test_status_code_200_and_uses_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "taxi/driver_confirm_delete.html")
        self.assertEqual(response.status_code, 200)

    def test_delete_driver(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("taxi:driver-list"))
        self.assertEqual(Driver.objects.count(), 1)
