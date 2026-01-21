from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver


class DriverListViewTest(TestCase):

    DRIVER_URL = reverse("taxi:driver-list")

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test", password="<PASSWORD>"
        )
        number_of_drivers = 13
        for i in range(number_of_drivers):
            Driver.objects.create_user(
                username=f"driver{i}",
                password="testpass123",
                license_number=f"ABC1234{i}",
                first_name=f"First{i}",
                last_name=f"Last{i}"
            )

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_pagination_is_five(self):
        self.client.force_login(self.user)
        response = self.client.get(self.DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_lists_all_cars(self):
        self.client.force_login(self.user)
        response = self.client.get(self.DRIVER_URL + "?page=3")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 4)


class DriverSearchFormTest(TestCase):
    DRIVER_URL = reverse("taxi:driver-list")

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test", password="testpass123"
        )
        number_of_drivers = 13
        for i in range(number_of_drivers):
            Driver.objects.create_user(
                username=f"driver{i}",
                password="testpass123",
                license_number=f"ABC1234{i}",
                first_name=f"First{i}",
                last_name=f"Last{i}"
            )

    def test_search_form_in_context(self):
        self.client.force_login(self.user)
        response = self.client.get(self.DRIVER_URL + "?first_name=driver")
        self.assertIn("search_form", response.context)
        self.assertEqual(
            response.context["search_form"].initial["first_name"], "driver"
        )

    def test_driver_queryset_filtered_by_first_name(self):
        self.client.force_login(self.user)

        Driver.objects.create_user(
            username="driverA",
            password="testpass",
            license_number="XYZ111",
            first_name="Alex"
        )
        Driver.objects.create_user(
            username="driverB",
            password="testpass",
            license_number="XYZ222",
            first_name="Bob"
        )

        response = self.client.get(self.DRIVER_URL + "?first_name=Alex")

        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertEqual(
            response.context["search_form"].initial["first_name"], "Alex"
        )

        drivers = response.context["driver_list"]
        self.assertEqual(len(drivers), 1)
        self.assertEqual(drivers[0].first_name, "Alex")


class DriverCreateViewTest(TestCase):
    DRIVER_URL = reverse("taxi:driver-create")

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test", password="<PASSWORD>"
        )

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_success_url(self):
        self.client.force_login(self.user)

        form_data = {
            "username": "driver123",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "license_number": "XYZ12345"
        }

        response = self.client.post(
            reverse("taxi:driver-create"), data=form_data
        )
        self.assertRedirects(response, reverse("taxi:driver-list"))
        self.assertTrue(Driver.objects.filter(username="driver123").exists())

    def test_form_displayed(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")
        self.assertContains(response, "license_number")

    def test_create_with_invalid_data(self):
        self.client.force_login(self.user)

        form_data = {

            "password1": "testpassword123",
            "password2": "testpassword123",
            "license_number": "XYZ12345"
        }
        response = self.client.post(
            reverse("taxi:driver-create"), data=form_data
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "username", "This field is required."
        )
        self.assertEqual(Car.objects.count(), 0)


class DriverDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test", password="12345"
        )
        cls.driver = Driver.objects.create(
            username="driverA",
            first_name="FirstA",
            last_name="LastA",
            license_number="ABC12345",
        )

        cls.DRIVER_URL = reverse(
            "taxi:driver-detail", kwargs={"pk": cls.driver.pk}
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.DRIVER_URL)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_view_uses_correct_template(self):
        self.client.force_login(self.user)
        response = self.client.get(self.DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")
        self.assertContains(response, "driverA")

    def test_404_if_driver_not_found(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:driver-detail", args=[9999]))
        self.assertEqual(response.status_code, 404)


class DriverUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test", password="<PASSWORD>"
        )

        cls.driver = Driver.objects.create(license_number="XYZ12345")

        cls.DRIVER_URL = reverse("taxi:driver-update", args=[cls.driver.id])

    def test_view_url_accessible_by_name(self):
        response = self.client.get(self.DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_view_uses_correct_template_after_update(self):
        self.client.force_login(self.user)
        response = self.client.post(
            self.DRIVER_URL,
            data={
                "username": "driverA",
                "password1": "<PASSWORD>",
                "password2": "<PASSWORD>",
                "license_number": "XYZ12345"
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertRedirects(response, reverse("taxi:driver-list"))
        self.assertContains(response, "XYZ12345")

    def test_update_with_invalid_data(self):
        self.client.force_login(self.user)
        url = reverse("taxi:driver-update", args=[self.driver.id])

        form_data = {
            "username": "driverA",
            "license_number": "",
        }

        response = self.client.post(url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, "form", "license_number", "This field is required."
        )

        self.driver.refresh_from_db()
        self.assertEqual(self.driver.license_number, "XYZ12345")


class DriverDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="test", password="pass123"
        )
        cls.driver = Driver.objects.create(
            username="driver_to_delete",
            license_number="DEL12345"
        )
        cls.url = reverse("taxi:driver-delete", args=[cls.driver.id])

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_delete_driver(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("taxi:driver-list"))
        self.assertFalse(Driver.objects.filter(id=self.driver.id).exists())

    def test_template_used(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_confirm_delete.html")
