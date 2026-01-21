from django.test import TestCase

from django.urls import reverse


class PublicViewTest(TestCase):
    def test_login_required(self):
        response_driver_list = self.client.get(reverse("taxi:driver-list"))
        response_car_list = self.client.get(reverse("taxi:car-list"))
        response_manufacturer_list = self.client.get(
            reverse("taxi:manufacturer-list")
        )
        resp_login = self.client.get(reverse("login"))
        resp_index = self.client.get(reverse("taxi:index"))

        self.assertEqual(response_driver_list.status_code, 302)
        self.assertEqual(response_car_list.status_code, 302)
        self.assertEqual(response_manufacturer_list.status_code, 302)
        self.assertEqual(resp_index.status_code, 302)
        self.assertEqual(resp_login.status_code, 200)
