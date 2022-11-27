from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", args=[1])
DRIVER_CREATE_URL = reverse("taxi:driver-create")


class PublicDriverTest(TestCase):
    def test_driver_list_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_driver_detail_login_required(self):
        res = self.client.get(DRIVER_DETAIL_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_driver_create_login_required(self):
        res = self.client.get(DRIVER_CREATE_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_driver",
            password="driver1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_driver_list(self):
        get_user_model().objects.create_user(
            username="driver1",
            first_name="first_name_1",
            last_name="last_name_1",
            license_number="AAA00000",
        )
        get_user_model().objects.create_user(
            username="driver2",
            first_name="first_name_2",
            last_name="last_name_2",
            license_number="BBB00000",
        )

        res = self.client.get(DRIVER_LIST_URL)

        drivers = get_user_model().objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(
            response=res,
            template_name="taxi/driver_list.html"
        )

    def test_retrieve_driver_detail(self):
        get_user_model().objects.create_user(
            username="driver1",
            first_name="first_name_1",
            last_name="last_name_1",
            license_number="AAA00000",
        )

        res = self.client.get(DRIVER_DETAIL_URL)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(
            response=res,
            template_name="taxi/driver_detail.html"
        )

    def test_driver_create(self):
        form_data = {
            "username": "test",
            "password1": "test1234test",
            "password2": "test1234test",
            "license_number": "AAA00000",
            "first_name": "Test",
            "last_name": "Testson"
        }
        self.client.post(DRIVER_CREATE_URL, data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])
