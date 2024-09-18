from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer
from django.contrib.auth import get_user_model


class ManufacturerSearchTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin", password="password123"
        )
        self.client.login(username="admin", password="password123")

        self.manufacturer1 = Manufacturer.objects.create(name="Toyota")
        self.manufacturer2 = Manufacturer.objects.create(name="Honda")
        self.manufacturer3 = Manufacturer.objects.create(name="Ford")

    def test_search_by_name(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list") + "?q=Toyota"
        )
        self.assertContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer2.name)
        self.assertNotContains(response, self.manufacturer3.name)

    def test_update_manufacturer(self):
        url = reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": self.manufacturer1.pk}
        )
        form_data = {"name": "UpdatedName", "country": "Japan"}
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)
        self.manufacturer1.refresh_from_db()
        self.assertEqual(self.manufacturer1.name, "UpdatedName")
