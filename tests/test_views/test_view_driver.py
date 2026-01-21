from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import DriverCreationForm, DriverLicenseUpdateForm

DRIVER_URL = reverse("taxi:driver-list")

DRIVERS_DATA = {
    "username": "test",
    "license_number": "ABC12345",
    "password1": "Test1234q",
    "password2": "Test1234q"
}


class PublicDriverFormatTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarFormatTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        get_user_model().objects.create_user(
            username="somebody",
            password="test123",
            license_number="SOM12345"
        )

        self.client.force_login(self.user)
        for i in range(1, 5):
            get_user_model().objects.create_user(
                username=f"test_0{i}",
                password="test123",
                license_number="TES" + f"{i}" * 5
            )

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user1234test",
            "password2": "user1234test",
            "first_name": "Test first",
            "last_name": "Test last",
            "license_number": "TES12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_searching_driver_find_existing_and_relevant(self):
        response = self.client.get(DRIVER_URL, data={"param": "test"})
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "test_01")
        self.assertContains(response, "test_02")
        self.assertNotContains(response, "somebody")

    def test_search_driver_not_found(self):
        response = self.client.get(DRIVER_URL, data={"param": "GG"})
        self.assertEqual(response.status_code, 200)

    def test_searching_drivers_find_all_if_name_empty(self):
        response = self.client.get(DRIVER_URL, {"username": ""})
        self.assertContains(response, "test_01")
        self.assertContains(response, "test_02")
        self.assertContains(response, "somebody")


class DriverChangeTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            license_number="ABC12346",
            password="Test1234q",
        )

        self.client.force_login(self.user)

    def test_successful_driver_creation(self):
        response = self.client.post(
            reverse("taxi:driver-create"),
            data=DRIVERS_DATA
        )
        driver = get_user_model().objects.get(username="test")
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            get_user_model().objects.filter(username="test").exists()
        )
        self.assertRedirects(
            response, reverse(
                "taxi:driver-detail",
                kwargs={"pk": driver.pk}
            )
        )

    def test_unsuccessful_driver_creation(self):
        data = {"username": "test"}
        response = self.client.post(reverse("taxi:driver-create"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            get_user_model().objects.filter(username="test").exists()
        )

    def test_driver_update_redirects_to_success_url(self):
        response = self.client.post(
            reverse(
                "taxi:driver-update",
                kwargs={"pk": self.user.pk}
            ),
            data={"license_number": "CBA54321"}
        )
        self.assertRedirects(response, reverse("taxi:driver-list"))

    def test_driver_creation_form_displayed_on_page(self):
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertIsInstance(response.context["form"], DriverCreationForm)

    def test_driver_successful_deletion_redirects_to_success_url(self):
        self.client.post(
            reverse(
                "taxi:driver-delete",
                kwargs={"pk": self.user.pk}

            )
        )
        self.assertFalse(get_user_model().objects.filter(pk=self.user.pk)
                         .exists())
