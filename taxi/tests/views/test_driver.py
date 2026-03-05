from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver
from taxi.views import DriverListView


class DriverListTest(TestCase):

    def setUp(self):
        user = Driver.objects.create_user(
            username="test",
            password="testpassword"
        )
        self.client.force_login(user)
        self.response = self.client.get(reverse("taxi:driver-list"))

    def test_get_page(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertEqual(DriverListView.paginate_by, 5)

    def test_get_context(self):
        self.assertIn("search", self.response.context)
