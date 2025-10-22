from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from taxi.models import Manufacturer

MANUFACTURER_URL = "/manufacturers/"

class PublicIndexTest(TestCase):
    def test_login_required(self):
        response = self.client.get("/")
        self.assertNotEqual(response.status_code, 200)


class PrivateIndexTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password",
        )
        self.client.force_login(self.user)




class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)



class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Test name", country="Test country")
        Manufacturer.objects.create(name="Test name 2", country="Test country 2")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["manufacturer_list"]), list(Manufacturer.objects.all()))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

