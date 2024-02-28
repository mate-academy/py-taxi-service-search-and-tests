from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

DRIVER_PK = 2
DRIVER_LIST_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", kwargs={"pk": DRIVER_PK})


class PublicDriverViewsTest(TestCase):
    def test_login_required(self):
        for url in [DRIVER_DETAIL_URL, DRIVER_LIST_URL]:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)


class PrivateDriverViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="papajoe",
            password="$ecreT_550",
            license_number="MAN99901"
        )
        self.client.force_login(self.user)

        self.driver = get_user_model().objects.create(
            username="elTerminator",
            password="$ecreT_505",
            license_number="MAN99001"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Bumga Gamga",
            country="Poltava"
        )
        self.car = Car.objects.create(
            model="Enzo",
            manufacturer=self.manufacturer
        )

    def test_driver_list_url_response(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_list_has_drivers(self):
        response = self.client.get(DRIVER_LIST_URL)
        all_drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(all_drivers)
        )

    def test_driver_search_form_exists(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertContains(response, "Search by username")

    def test_driver_search_form_works_correctly(self):
        response = self.client.get(f"{DRIVER_LIST_URL}?username=t")
        self.assertEqual(
            list(response.context["driver_list"]), [self.driver]
        )

    def test_driver_detail_view_shows_all_info(self):
        self.car.drivers.add(self.driver)
        response = self.client.get(DRIVER_DETAIL_URL)
        page_content = response.content.decode("utf-8")

        self.assertIn(self.driver.username, page_content)
        self.assertIn(self.driver.license_number, page_content)
        self.assertIn(str(self.car), page_content)
