from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


from ..models import Manufacturer


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="<PASSWORD>",
        )

        self.client.force_login(self.user)

    def test_search(self) -> None:
        country = "<COUNTRY>"

        Manufacturer.objects.bulk_create([
            Manufacturer(name="AAA Test1", country=country),
            Manufacturer(name="AAA Test2", country=country),
            Manufacturer(name="BBB Test1", country=country),
            Manufacturer(name="BBB Test2", country=country),
        ])

        res = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"title": "AAA"}
        )

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "AAA Test1")
        self.assertContains(res, "AAA Test2")
        self.assertNotContains(res, "BBB Test1")
        self.assertNotContains(res, "BBB Test2")
