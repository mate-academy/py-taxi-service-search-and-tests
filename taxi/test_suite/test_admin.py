from django.test import TestCase
from taxi.admin import CarAdmin


class CarAdminTest(TestCase):
    def test_list_display(self):
        self.assertIn("model", CarAdmin.list_display)
        self.assertIn("manufacturer", CarAdmin.list_display)
