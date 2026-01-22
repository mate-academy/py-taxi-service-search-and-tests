from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


URL_MANUFACTURER_LIST = "taxi:manufacturer-list"


class PublicManufacturerViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="krixn",
            password="1337",
        )

    def test_manufacturer_login_required(self):
        response = self.client.get(reverse(URL_MANUFACTURER_LIST))

        self.assertRedirects(
            response,
            f"/accounts/login/?next={reverse(URL_MANUFACTURER_LIST)}"
        )
