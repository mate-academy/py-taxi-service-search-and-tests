from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
MANUFACTURER_UPDATE_URL = reverse("taxi:manufacturer-update", kwargs={"pk": 1})
MANUFACTURER_DELETE_URL = reverse("taxi:manufacturer-delete", kwargs={"pk": 1})


class PublicDriverTest(TestCase):

    def test_login_required(self):
        for url in (
                MANUFACTURER_LIST_URL,
                MANUFACTURER_CREATE_URL,
                MANUFACTURER_UPDATE_URL,
                MANUFACTURER_DELETE_URL,
        ):
            res = self.client.get(url)

            self.assertNotEqual(res.status_code, 200)


class ManufacturerPrivateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_username",
            password="test1234",
        )
        self.client.force_login(self.user)

        self.first_manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.second_manufacturer = Manufacturer.objects.create(
            name="Mercedes Benz",
            country="Germany"
        )


    def test_manufacturers_search(self):
        url = f"{MANUFACTURER_LIST_URL}?name=be"
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertIn("search_form", res.context)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            [self.second_manufacturer]
        )


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

    def test_retrieve_drivers(self):
        res = self.client.get(DRIVER_LIST_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["driver_list"]),
            list(get_user_model().objects.all())
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_drivers_search_filter(self):
        url = f"{DRIVER_LIST_URL}?username=driver"
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertIn("search_form", res.context)
        self.assertEqual(list(res.context["driver_list"]), [self.driver])
