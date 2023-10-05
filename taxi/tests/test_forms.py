from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import DriverCreationForm
from taxi.models import Driver


class CreationFormTest(TestCase):
    def test_driver_creation_with_license_number_first_name_last_name(self) -> None:
        form_data = {
            "username": "user_test_form",
            "password1": "abc123def",
            "password2": "abc123def",
            "first_name": "Test name",
            "last_name": "Test surname",
            "license_number": "ABC12345"
        }
        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class DriverLicenceUpdateFormTest(TestCase):
    LICENCE_NUMBER = "ABC12345"

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)
        self.driver = Driver.objects.create(
            username="driver",
            license_number= self.LICENCE_NUMBER
        )

    def post_test_and_refresh_from_db(self, new_license_number) -> None:
        url = reverse("taxi:driver-update", kwargs={"pk": self.driver.pk})
        self.client.post(url, {"license_number": new_license_number})
        self.driver.refresh_from_db()
        self.assertNotEqual(self.driver.license_number, new_license_number)
        self.assertEqual(self.driver.license_number, self.LICENCE_NUMBER)

    def test_driver_license_form_without_letters(self) -> None:
        new_license_number = "1234678"
        self.post_test_and_refresh_from_db(new_license_number=new_license_number)

    def test_driver_licence_with_length_less_than_eight(self) -> None:
        new_license_number = "AMV1234"
        self.post_test_and_refresh_from_db(new_license_number=new_license_number)

    def test_driver_licence_without_numberss(self) -> None:
        new_license_number = "ABCDEFGH"
        self.post_test_and_refresh_from_db(new_license_number=new_license_number)

    def test_driver_licence_with_incorrect_proportion_of_chars_and_nums(self) -> None:
        new_license_number = "ABCDEF12"
        self.post_test_and_refresh_from_db(new_license_number=new_license_number)
        new_license_number = "AB015612"
        self.post_test_and_refresh_from_db(new_license_number=new_license_number)
        new_license_number = "76915ABC"
        self.post_test_and_refresh_from_db(new_license_number=new_license_number)


class TestDriverUsernameSearchForm(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="abc123def",
        )
        self.client.force_login(self.user)

        get_user_model().objects.create_user(
            username="andrew",
            password="adc123def",
            license_number="ABCD5612",
        )
        get_user_model().objects.create_user(
            username="john",
            password="abc123def",
            license_number="ABED5632",
        )
        get_user_model().objects.create_user(
            username="mary",
            password="abc123def",
            license_number="ABED5932",
        )

    def get_response(self,form_data) -> None:
        url = reverse("taxi:driver-list")
        return self.client.get(url, data=form_data)

    def test_driver_search_form_with_full_match(self) -> None:
        form_data = {"username": "john"}
        response = self.get_response(form_data)
        self.assertContains(response, form_data["username"])

    def test_driver_search_form_with_partial_match(self) -> None:
        form_data = {"username": "ma"}
        response = self.get_response(form_data)
        self.assertContains(response, form_data["username"])

    def test_driver_search_form_with_empty_field(self) -> None:
        form_data = {"username": ""}
        response = self.get_response(form_data)
        self.assertContains(response, "mary")
        self.assertContains(response, "andrew")
        self.assertContains(response, "john")

    def test_driver_search_form_with_no_matches(self) -> None:
        form_data = {"username": "angelina"}
        response = self.get_response(form_data)
        self.assertNotContains(response, "andrew")
        self.assertNotContains(response, "john")
