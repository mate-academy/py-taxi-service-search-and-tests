from django.test  import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer


class ViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="test_user",
            password="User12345"
        )
        self.client.force_login(self.user)

    def test_manufacturer_list(self):
        Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )
        response = self.client.get(
            reverse("taxi:manufacturer-list")
        )
        self.assertEquals(response.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEquals(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )
