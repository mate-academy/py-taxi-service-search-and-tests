from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car

User = get_user_model()


class SearchTests(TestCase):
    def setUp(self):
        # cria usuário e loga
        self.user = User.objects.create_user(
            username="admin", password="testpass123", license_number="ABC12345"
        )
        self.client.login(username="admin", password="testpass123")

        # fabricantes e carros
        self.manufacturer = Manufacturer.objects.create(name="Toyota")
        self.other_manufacturer = Manufacturer.objects.create(name="Ford")
        self.car1 = Car.objects.create(model="Corolla", manufacturer=self.manufacturer)
        self.car2 = Car.objects.create(model="Yaris", manufacturer=self.manufacturer)
        self.other_car = Car.objects.create(model="Focus", manufacturer=self.other_manufacturer)

    def test_search_driver_by_username(self):
        response = self.client.get(reverse("taxi:driver-list"), {"search": "adm"})
        self.assertContains(response, "admin")
        # garantir que outro nome não aparece (se existirem)
        self.assertNotContains(response, "some-other-user")

    def test_search_car_by_model(self):
        # busca parcial por "corol" encontra "Corolla"
        response = self.client.get(reverse("taxi:car-list"), {"search": "corol"})
        self.assertContains(response, "Corolla")
        # e não deve conter carros não relacionados
        self.assertNotContains(response, "Yaris")  # Yaris não contém "corol"
        self.assertNotContains(response, "Focus")

    def test_search_manufacturer_by_name(self):
        response = self.client.get(reverse("taxi:manufacturer-list"), {"search": "toy"})
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")
