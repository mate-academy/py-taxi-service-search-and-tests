from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicDriverTests(TestCase):
    def test_login_required(self):

        driver = get_user_model().objects.create_user(
            username="test_username",
            password="test_1234"
        )

        driver_detail_url = reverse("taxi:car-detail", kwargs={"pk": driver.pk})

        driver_urls = [DRIVER_LIST_URL, driver_detail_url]

        for url in driver_urls:
            response = self.client.get(url)

            self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_username_1",
            password="test_1234",
            license_number="TES12349"
        )

        get_user_model().objects.create_user(
            username="test_username_2",
            password="test_1234",
            license_number="TES12340"
        )

        self.client.force_login(self.user)

    def test_retrieve_driver_list(self):
        response = self.client.get(DRIVER_LIST_URL)

        drivers = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_driver_detail(self):
        driver_detail_url = reverse("taxi:driver-detail", kwargs={"pk": self.user.pk})

        response = self.client.get(driver_detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["driver"],
            self.user
        )
        self.assertTemplateUsed(response, "taxi/driver_detail.html")


