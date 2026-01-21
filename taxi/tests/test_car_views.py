from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car
from taxi.tests import fixtures

LIST_URL = reverse("taxi:car-list")
CREATE_URL = reverse("taxi:car-create")
UPDATE_URL = reverse("taxi:car-update", kwargs={"pk": 1})
DELETE_URL = reverse("taxi:car-delete", kwargs={"pk": 1})
LOGIN_URL = reverse("login")


class PublicCarViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        fixtures.fill_db()

    def test_list_view_login_required_and_redirect(self):
        response = self.client.get(LIST_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"{LOGIN_URL}?next={LIST_URL}")

    def test_create_view_login_required_and_redirect(self):
        response = self.client.get(CREATE_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"{LOGIN_URL}?next={CREATE_URL}")

    def test_update_view_login_required_and_redirect(self):
        response = self.client.get(UPDATE_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"{LOGIN_URL}?next={UPDATE_URL}")

    def test_delete_view_login_required_and_redirect(self):
        response = self.client.get(DELETE_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"{LOGIN_URL}?next={DELETE_URL}")


class PrivateCarViewTests(TestCase):
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
        self.assertEqual(len(response.context.get("car_list")), 5)

    def test_list_view_correct_num_of_entries_on_next_page(self):
        response = self.client.get(LIST_URL + "?page=3")

        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context.get("is_paginated"))
        self.assertEqual(len(response.context.get("car_list")), 2)

    def test_list_view_context_contain_search_by_model_and_it_works(self):
        response = self.client.get(LIST_URL + "?model=i")
        cars_ = list(response.context.get("car_list").values("model"))

        self.assertIn("search_form", response.context)
        self.assertTrue(len(cars_) == 4)
        self.assertCountEqual(fixtures.custom_cars, cars_)

    def test_create_view(self):
        data = {"model": "custom_car", "manufacturer": 8, "drivers": [1, 2, 3]}

        response = self.client.post(CREATE_URL, data)

        self.assertRedirects(response, LIST_URL)
        self.assertTrue(Car.objects.filter(model="custom_car").exists())

    def test_update_view(self):
        data = {
            "model": "custom_model", "manufacturer": 8, "drivers": [1, 2, 3]
        }
        before = Car.objects.get(pk=1)

        response = self.client.post(UPDATE_URL, data)
        after = Car.objects.get(pk=1)

        self.assertRedirects(response, LIST_URL)
        self.assertEqual(after.model, "custom_model")
        self.assertEqual(after.manufacturer_id, 8)
        self.assertEqual(after.id, before.id)

    def test_delete_view(self):
        response = self.client.post(DELETE_URL)

        self.assertRedirects(response, LIST_URL)
        self.assertFalse(Car.objects.filter(pk=1).exists())
