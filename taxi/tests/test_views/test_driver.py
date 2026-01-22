from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Driver, Manufacturer, Car


DRIVER_URL = reverse("taxi:driver-list")


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser", password="<PASSWORD>"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        res = self.client.get(DRIVER_URL)
        self.assertEqual(res.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(list(res.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(res, "taxi/driver_list.html")
        self.assertTrue(res.context["search_form"])
