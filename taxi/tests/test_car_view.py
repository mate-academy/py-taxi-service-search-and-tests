from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

CAR_URL = reverse("taxi:car-list")


class PublicCarViewTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEquals(response.status_code, 200)


class PrivateCarViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            email="<EMAIL>",
            password="<PASSWORD>")
        self.client.force_login(self.user)

    def test_retrieve_car_view(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_update_car_view(self):
        manufacturer = Manufacturer.objects.create(name="mercedes")
        c4 = Car.objects.create(model="c4", manufacturer=manufacturer)
        c4.manufacturer = manufacturer
        c4.model = "c4 AMG"

        c4.save()

        update_c4 = Car.objects.get(pk=c4.id)

        self.assertEqual(update_c4.model, "c4 AMG")

    def test_delete_car_view(self):
        manufacturer = Manufacturer.objects.create(name="mercedes")
        c4 = Car.objects.create(model="c4", manufacturer=manufacturer)
        self.assertEqual(Car.objects.count(), 1)
        c4.delete()
        self.assertEqual(Car.objects.count(), 0)
