from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse

from taxi.models import Car, Manufacturer
from taxi.views import DriverListView, DriverDetailView

DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PublicDriverTests(TestCase):

    def test_login_required_driver_list_url(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_driver_create_url(self):
        response = self.client.get(DRIVER_CREATE_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_driver_detail_url(self):
        self.driver = get_user_model().objects.create_user(
            username="test_man", password="qwerty4321")
        response = self.client.get(reverse(
            "taxi:driver-detail", kwargs={"pk": self.driver.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_login_required_driver_update_url(self):
        self.driver = get_user_model().objects.create_user(
            username="test_man", password="qwerty4321")
        response = self.client.get(reverse(
            "taxi:driver-update", kwargs={"pk": self.driver.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_login_required_driver_delete_url(self):
        self.driver = get_user_model().objects.create_user(
            username="test_man", password="qwerty4321")
        response = self.client.get(reverse(
            "taxi:driver-delete", kwargs={"pk": self.driver.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user_login",
            password="password11",
            license_number="ASD12345",
        )
        self.client.force_login(self.user)
        for driver in range(3):
            self.driver = get_user_model().objects.create_user(
                username="test_user" + str(driver),
                password="password1122",
                license_number="ASD1234" + str(driver),
            )

    def test_get_data_from_driver_list(self):
        response = self.client.get(DRIVER_LIST_URL)
        drivers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_get_queryset_from_driver_list(self):
        """test that view return right filtered queryset"""
        response = RequestFactory().get("drivers/?username=3")
        view = DriverListView()
        view.request = response
        qs = view.get_queryset()

        self.assertQuerysetEqual(
            qs, get_user_model().objects.filter(username__icontains="3"))

    def test_create_driver(self):
        form_data = {
            "username": "vasa_test1",
            "password1": "qwerty12345test1",
            "password2": "qwerty12345test1",
            "first_name": "vasa_test1",
            "last_name": "chak_test1",
            "license_number": "ARE33445"
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(new_driver.license_number, form_data["license_number"])
