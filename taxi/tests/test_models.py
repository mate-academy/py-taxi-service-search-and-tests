from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create(
            username="driver-1",
            password="django1234",
        )
        self.client.force_login(self.driver)

    def test_driver_get_absolute_url(self):
        driver = get_user_model().objects.get(id=1)
        # This will also fail if the URLConf is not defined.
        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail", args=["1"])
        )
