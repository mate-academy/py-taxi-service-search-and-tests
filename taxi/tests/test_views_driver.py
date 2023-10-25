from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import DriverSearchForm
from taxi.models import Driver

DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")
DRIVER_UPDATE_URL = reverse("taxi:driver-update", args=["1"])
DRIVER_DELETE_URL = reverse("taxi:driver-delete", args=["1"])


class PublicDriverTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_list_required(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_create_required(self):
        response = self.client.get(DRIVER_CREATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_update_required(self):
        response = self.client.get(DRIVER_UPDATE_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_login_delete_required(self):
        Driver.objects.create(
            username="Test",
            password="Test123"
        )
        response = self.client.get(DRIVER_DELETE_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverListTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="Test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_content(self):
        response = self.client.get(DRIVER_LIST_URL)
        driver_list = Driver.objects.all()

        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver_list)
        )

    def test_template(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_type_of_search_form(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(
            type(response.context["search_form"]),
            type(DriverSearchForm())
        )


class PrivateDriverCreateTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="Test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver_create(self):
        response = self.client.get(DRIVER_CREATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(DRIVER_CREATE_URL)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_create_driver(self):
        form_data = {
            "username": "Test_user",
            "password1": "testPass1",
            "password2": "testPass1",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "ABC12345",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.username, form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class PrivateDriverUpdateTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="Test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver_create(self):
        response = self.client.get(DRIVER_UPDATE_URL)
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(DRIVER_UPDATE_URL)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_success_url(self):
        response = self.client.get(DRIVER_UPDATE_URL)
        self.assertEqual(
            response.context_data["view"].success_url,
            reverse("taxi:driver-list")
        )


class PrivateDriverDeleteTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Test",
            password="Test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver_create(self):
        response = self.client.get(DRIVER_DELETE_URL)
        self.assertEqual(response.status_code, 200)

    def test_template(self):
        response = self.client.get(DRIVER_DELETE_URL)
        self.assertTemplateUsed(response, "taxi/driver_confirm_delete.html")
