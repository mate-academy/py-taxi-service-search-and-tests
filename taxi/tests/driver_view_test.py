from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_URL = reverse("taxi:driver-create")
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", kwargs={"pk": 1})
DRIVER_UPDATE_URL = reverse("taxi:driver-update", kwargs={"pk": 1})
DRIVER_DELETE_URL = reverse("taxi:driver-delete", kwargs={"pk": 1})


class PublicDriverTest(TestCase):

    def test_login_required(self):
        for url in (
                DRIVER_LIST_URL,
                DRIVER_CREATE_URL,
                DRIVER_DETAIL_URL,
                DRIVER_UPDATE_URL,
                DRIVER_DELETE_URL,
        ):
            res = self.client.get(url)

            self.assertNotEqual(res.status_code, 200)


class DriverPrivateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test1234",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

        self.driver = get_user_model().objects.create_user(
            username="driver_username",
            password="driver1234",
            license_number="ABC54321"
        )

    def test_list_drivers(self):
        res = self.client.get(DRIVER_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["driver_list"]),
            list(get_user_model().objects.all())
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")

