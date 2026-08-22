from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


def create_drivers(count):
    for i in range(count):
        get_user_model().objects.create_user(
            username=f"username{i}",
            password=f"password{i}",
            license_number=f"DRV{i:05d}",
        )


class TestDriverListView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="ABC12345", )

        self.url = reverse("taxi:driver-list")

    def test_logged_user_can_access(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_anonymous_redirect_to_login(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")
        self.assertEqual(response.status_code, 302)

    def test_context_of_listing_drivers(self):
        self.client.force_login(self.user)
        create_drivers(6)

        response = self.client.get(self.url)
        drivers = response.context["driver_list"]

        self.assertEqual(drivers.count(), 5)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_user_by_username(self):
        self.client.force_login(self.user)
        create_drivers(6)
        main_driver = get_user_model().objects.create_user(
            username="cwelcio",
            password="cwelcio123",
            license_number="QWE54321")

        response = self.client.get(self.url, {"username": "CWELCIO"})
        drivers = response.context["driver_list"]

        self.assertEqual(drivers.count(), 1)
        self.assertIn(main_driver, drivers)

    def test_listing_without_query_param(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)
        drivers = response.context["driver_list"]

        self.assertEqual(drivers.count(), 1)
        self.assertIn(self.user, drivers)

    def test_pagination(self):
        self.client.force_login(self.user)
        create_drivers(6)

        response = self.client.get(self.url)

        page_obj = response.context["page_obj"]
        drivers = response.context["driver_list"]

        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(drivers.count(), 5)
        self.assertTrue(page_obj.has_next())
        self.assertFalse(page_obj.has_previous())
        self.assertEqual(page_obj.number, 1)
        self.assertEqual(page_obj.paginator.num_pages, 2)

    def test_pagination_second_page(self):
        self.client.force_login(self.user)
        create_drivers(6)

        response = self.client.get(
            self.url,
            {"page": 2}
        )

        drivers = response.context["driver_list"]
        page_obj = response.context["page_obj"]

        self.assertEqual(drivers.count(), 2)
        self.assertEqual(page_obj.number, 2)
        self.assertTrue(page_obj.has_previous())
        self.assertFalse(page_obj.has_next())


class TestDriverDetailView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="ABC12345", )
        self.url = reverse("taxi:driver-detail", kwargs={"pk": self.user.pk})

    def test_logged_user_can_access(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_anonymous_redirect_to_login(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")
        self.assertEqual(response.status_code, 302)

    def test_driver_detail_view(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)
        driver = response.context["driver"]

        self.assertEqual(self.user.cars.count(), 0)
        self.assertEqual(self.user, driver)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_nonexisting_driver_gives_404(self):
        self.client.force_login(self.user)

        url = reverse("taxi:driver-detail",
                      kwargs={"pk": 55555})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


class TestDriverCreateView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="ABC12345", )
        self.url = reverse("taxi:driver-create")

    def test_logged_user_can_access(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_anonymous_redirect_to_login(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")
        self.assertEqual(response.status_code, 302)

    def test_used_template(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_create_of_driver(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.url,
            {"username": "Tom",
             "password1": "StrongPassword123!",
             "password2": "StrongPassword123!",
             "license_number": "QWE54321",
             "first_name": "tomek",
             "last_name": "tomeczek"})

        driver = get_user_model().objects.get(username="Tom")

        self.assertEqual(driver.username, "Tom")
        self.assertEqual(get_user_model().objects.count(), 2)
        self.assertEqual(driver.license_number, "QWE54321")
        self.assertEqual(driver.first_name, "tomek")
        self.assertEqual(driver.last_name, "tomeczek")
        self.assertRedirects(
            response,
            reverse("taxi:driver-detail",
                    kwargs={"pk": driver.pk}))

    def test_creation_of_driver_with_wrong_data(self):
        self.client.force_login(self.user)

        response = self.client.post(
            self.url,
            {"username": "Tom",
             "password1": "StrongPassword123!",
             "password2": "StrongPassword123!",
             "license_number": "ABC12345",
             "first_name": "tomek",
             "last_name": "tomeczek"})
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertFalse(
            get_user_model().objects.filter(username="Tom").exists()
        )
        self.assertIn("license_number", form.errors)


class TestDriverDeleteView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="ABC12345",
        )

        self.driver_to_delete = get_user_model().objects.create_user(
            username="delete_me",
            password="test123",
            license_number="DEL12345",
        )

        self.url = reverse(
            "taxi:driver-delete",
            kwargs={"pk": self.driver_to_delete.pk}
        )

    def test_logged_user_can_access(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_anonymous_redirect_to_login(self):
        response = self.client.get(self.url)

        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")
        self.assertEqual(response.status_code, 302)

    def test_deleting_driver(self):
        self.client.force_login(self.user)

        self.assertEqual(get_user_model().objects.count(), 2)

        response = self.client.post(self.url)

        self.assertEqual(get_user_model().objects.count(), 1)

        self.assertFalse(
            get_user_model().objects.filter(
                pk=self.driver_to_delete.pk
            ).exists()
        )

        self.assertRedirects(
            response,
            reverse("taxi:driver-list")
        )


class TestDriverLicenseUpdateView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
            license_number="ABC12345"
        )
        self.url = reverse("taxi:driver-update", kwargs={"pk": self.user.pk})

    def test_logged_user_can_access(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_anonymous_redirect_to_login(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next={self.url}")

    def test_updating_license_number(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url, {"license_number": "JKL93021"})

        self.user.refresh_from_db()

        self.assertEqual(self.user.license_number, "JKL93021")
        self.assertRedirects(response, reverse("taxi:driver-list"))

    def test_updating_license_number_in_wrong_format(self):
        self.client.force_login(self.user)

        response = self.client.post(self.url, {"license_number": "32132121"})
        form = response.context["form"]

        self.user.refresh_from_db()

        self.assertFalse(form.is_valid())
        self.assertEqual(self.user.license_number, "ABC12345")
        self.assertEqual(response.status_code, 200)
        self.assertIn("license_number", form.errors)
