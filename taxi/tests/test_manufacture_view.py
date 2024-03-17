from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer

MANUFACTURE_URL = reverse("taxi:manufacturer-list")


class PublicManufactureViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURE_URL)
        self.assertNotEquals(response.status_code, 200)


class PrivateManufactureViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            email="<EMAIL>",
            password="<PASSWORD>")
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Mercedes")
        Manufacturer.objects.create(name="BMW")

        response = self.client.get(MANUFACTURE_URL)
        self.assertEquals(response.status_code, 200)

    def test_update_manufacturers(self):
        mercedes = Manufacturer.objects.create(name="Mercedes")
        bmw = Manufacturer.objects.create(name="BMW")
        mercedes.name = "Mercedes-Benz"
        bmw.name = "BMW AG"

        mercedes.save()
        bmw.save()

        update_mercedes = Manufacturer.objects.get(pk=mercedes.id)
        update_bmw = Manufacturer.objects.get(pk=bmw.id)

        self.assertEquals(update_mercedes.name, "Mercedes-Benz")
        self.assertEquals(update_bmw.name, "BMW AG")

    def test_delete_manufacturers(self):
        mercedes = Manufacturer.objects.create(name="mercedes")
        self.assertEqual(Manufacturer.objects.count(), 1)

        mercedes.delete()
        self.assertEqual(Manufacturer.objects.count(), 0)
