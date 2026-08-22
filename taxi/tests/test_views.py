from django.test import TestCase
from django.urls import reverse


class AccessPermissionsTests(TestCase):
    def test_login_required_for_car_list(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 302)
