from django.test import TestCase
from django.urls import reverse
from taxi.models import Car, Manufacturer
from django.contrib.auth import get_user_model


class CarSearchTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin", password="password123"
        )
        self.client.login(username="admin", password="password123")

        self.manufacturer = Manufacturer.objects.create(name="TestMaker")
        self.car1 = Car.objects.create(
            model="ModelA",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="ModelB",
            manufacturer=self.manufacturer
        )
        self.car3 = Car.objects.create(
            model="ModelC",
            manufacturer=self.manufacturer
        )

    def test_search_by_model(self):
        response = self.client.get(reverse("taxi:car-list") + "?q=ModelA")
        self.assertContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)
        self.assertNotContains(response, self.car3.model)

    def test_delete_car(self):
        url = reverse("taxi:car-delete", kwargs={"pk": self.car1.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Car.objects.filter(pk=self.car1.pk).exists())
