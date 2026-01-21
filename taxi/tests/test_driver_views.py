from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.tests import fixtures

LIST_URL = reverse("taxi:driver-list")
CREATE_URL = reverse("taxi:driver-create")
LICENSE_UPDATE_URL = reverse("taxi:driver-update", kwargs={"pk": 1})
DELETE_URL = reverse("taxi:driver-delete", kwargs={"pk": 1})
DETAIL_URL = reverse("taxi:driver-detail", kwargs={"pk": 1})


class PublicDriverViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        fixtures.fill_db()

    def test_list_view_login_required_and_redirect(self):
        response = self.client.get(LIST_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'{reverse("login")}?next={LIST_URL}')

    def test_create_view_login_required_and_redirect(self):
        response = self.client.get(CREATE_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'{reverse("login")}?next={CREATE_URL}')

    def test_license_update_view_login_required_and_redirect(self):
        response = self.client.get(LICENSE_UPDATE_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response, f'{reverse("login")}?next={LICENSE_UPDATE_URL}'
        )

    def test_delete_view_login_required_and_redirect(self):
        response = self.client.get(DELETE_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f'{reverse("login")}?next={DELETE_URL}')


class PrivateDriverViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        fixtures.fill_db()

    def setUp(self):
        self.client.force_login(get_user_model().objects.get(pk=1))

    def test_list_view_is_paginated_by_5(self):
        response = self.client.get(LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context.get("is_paginated"))
        self.assertEqual(len(response.context.get("driver_list")), 5)

    def test_list_view_correct_num_of_entries_on_next_page(self):
        response = self.client.get(LIST_URL + "?page=3")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context.get("is_paginated"))
        self.assertEqual(len(response.context.get("driver_list")), 2)

    def test_list_view_context_contain_search_by_name_and_it_works(self):
        response = self.client.get(LIST_URL + "?username=admin")
        drivers_ = list(response.context.get("driver_list").values("username"))

        self.assertIn("search_form", response.context)
        self.assertTrue(len(drivers_) == 1)
        self.assertCountEqual([{"username": "admin"}], drivers_)

    def test_create_view(self):
        data = {
            "username": "custom_username",
            "first_name": "custom_first_name",
            "last_name": "custom_last_name",
            "password1": "1cust0om",
            "password2": "1cust0om",
            "email": "custom@email.com",
            "license_number": "LIC11111",
        }

        response = self.client.post(CREATE_URL, data)
        custom_driver = get_user_model().objects.last()

        self.assertRedirects(
            response,
            reverse("taxi:driver-detail", kwargs={"pk": custom_driver.pk})
        )
        self.assertTrue(
            get_user_model().objects.filter(
                username="custom_username"
            ).exists()
        )

    def test_license_update_view(self):
        data = {
            "license_number": "UPD11111",
        }
        before = get_user_model().objects.get(pk=1)

        response = self.client.post(LICENSE_UPDATE_URL, data)
        after = get_user_model().objects.get(pk=1)

        self.assertRedirects(response, LIST_URL)
        self.assertEqual(after.license_number, "UPD11111")
        self.assertEqual(after.id, before.id)

    def test_delete_view(self):
        response = self.client.post(DELETE_URL)

        self.assertTrue(response.status_code == 302)
        self.assertEqual(response.url, LIST_URL)
        self.assertFalse(get_user_model().objects.filter(pk=1).exists())
