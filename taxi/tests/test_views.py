from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverSearchForm
from taxi.models import Manufacturer

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "password"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="test_name", country="test_country")

        response = self.client.get(MANUFACTURERS_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "password"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "pass123word",
            "password2": "pass123word",
            "first_name": "first",
            "last_name": "last",
            "license_number": "AMD12345"
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class DriverSearchFormTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test",
            "password"
        )
        self.client.force_login(self.user)
        form_data1 = {
            "username": "user1",
            "password1": "pass123word1",
            "password2": "pass123word1",
            "first_name": "first1",
            "last_name": "last1",
            "license_number": "AMD12345"
        }
        form_data2 = {
            "username": "user2",
            "password1": "pass123word2",
            "password2": "pass123word2",
            "first_name": "first2",
            "last_name": "last2",
            "license_number": "AMD23456"
        }
        form_data3 = {
            "username": "another",
            "password1": "pass123word3",
            "password2": "pass123word3",
            "first_name": "first3",
            "last_name": "last3",
            "license_number": "AMD34567"
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data1)
        self.client.post(reverse("taxi:driver-create"), data=form_data2)
        self.client.post(reverse("taxi:driver-create"), data=form_data3)

    def test_search_with_valid_input(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "user"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertContains(response, "user1")
        self.assertContains(response, "user2")
        self.assertNotContains(response, "another")

    def test_search_with_invalid_input(self):
        response = self.client.get(reverse(
            "taxi:driver-list"),
            {"username": "nonexistent"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertNotContains(response, "user1")
        self.assertNotContains(response, "user2")
        self.assertNotContains(response, "another")

    def test_search_form_initial_data(self):
        response = self.client.get(reverse("taxi:driver-list"))
        form = response.context["search_form"]

        self.assertEqual(response.status_code, 200)
        self.assertTrue("search_form" in response.context)
        self.assertIsInstance(form, DriverSearchForm)
        self.assertEqual(form.initial["username"], "")

    def test_search_form_submission(self):
        response = self.client.get(reverse(
            "taxi:driver-list"),
            {"username": "user1"}
        )
        form = response.context["search_form"]

        self.assertEqual(response.status_code, 200)
        self.assertTrue("search_form" in response.context)
        self.assertIsInstance(form, DriverSearchForm)
        self.assertEqual(form.initial["username"], "user1")
        self.assertContains(response, 'value="user1"')

    def test_search_form_invalid_submission(self):
        response = self.client.get(reverse(
            "taxi:driver-list"),
            {"username": "aaaaa"}
        )
        form = response.context["search_form"]

        self.assertEqual(response.status_code, 200)
        self.assertTrue("search_form" in response.context)
        self.assertIsInstance(form, DriverSearchForm)
        self.assertContains(response, 'value="aaaaa"')
