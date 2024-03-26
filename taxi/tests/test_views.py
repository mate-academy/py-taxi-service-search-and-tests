from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

manufacturer_url = reverse("taxi:manufacturer-list")
driver_url = reverse("taxi:driver-list")
car_url = reverse("taxi:car-list")
index_url = reverse("taxi:index")


class PublicTest(TestCase):
    def test_manufacturer_login_required(self):
        res = self.client.get(manufacturer_url)
        self.assertNotEquals(res.status_code, 200)

    def test_driver_login_required(self):
        res = self.client.get(driver_url)
        self.assertNotEquals(res.status_code, 200)

    def test_car_login_required(self):
        res = self.client.get(car_url)
        self.assertNotEquals(res.status_code, 200)

    def test_index_login_required(self):
        res = self.client.get(index_url)
        self.assertNotEquals(res, 200)


class PrivateTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="<PASSWORD>",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(
            name="test",
            country="test",
        )
        Manufacturer.objects.create(
            name="test1",
            country="test1",
        )
        manufacturer = Manufacturer.objects.all()
        response = self.client.get(manufacturer_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturer)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_car_list(self):
        manufacturer = Manufacturer.objects.create(name="test", country="test")
        Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        Car.objects.create(
            model="test2",
            manufacturer=manufacturer,
        )
        car = Car.objects.all()
        response = self.client.get(car_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(car))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_driver_list(self):
        get_user_model().objects.create_user(
            license_number="ABC12345",
            username="test123",
            password="<PASSWORD>",
        )
        get_user_model().objects.create_user(
            license_number="ABC12346",
            username="test1234",
            password="<PASSWORD>1",
        )
        user = get_user_model().objects.all()
        response = self.client.get(driver_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(user))
        self.assertTemplateUsed(response, "taxi/driver_list.html")
