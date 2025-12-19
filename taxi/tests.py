from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        result = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(result.status_code, 200)
        self.assertTemplateUsed(result, "taxi/car_list.html")\


    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        car1 = Car.objects.create(model="Camry", manufacturer=manufacturer)
        car3 = Car.objects.create(model="Mustang", manufacturer=manufacturer)

        url = reverse("taxi:car-list") + "?model=Ca"
        result = self.client.get(url)
        self.assertContains(result, car1.model)
        self.assertNotContains(result, car3.model)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testadmin",
            password="password124"
        )
        self.client.force_login(self.user)

    def test_search_driver_by_username(self):
        user1 = get_user_model().objects.create_user(
            username="jake",
            password="123",
            license_number="AAA567891"
        )
        user2 = get_user_model().objects.create_user(
            username="dane",
            password="123",
            license_number="BBB567121"
        )

        url = reverse("taxi:driver-list") + "?username=ja"
        result = self.client.get(url)
        self.assertContains(result, user1.username)
        self.assertNotContains(result, user2.username)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.force_login(self.user)

    def test_search_manufacturer_by_name(self):
        manufacturer1 = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

        url = reverse("taxi:manufacturer-list") + "?name=Tes"
        result = self.client.get(url)
        self.assertContains(result, manufacturer1.name)
        self.assertNotContains(result, manufacturer2.name)
