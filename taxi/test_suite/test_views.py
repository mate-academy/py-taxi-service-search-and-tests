from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Driver, Car, Manufacturer


User = get_user_model()


class ViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="alex", password="12345")
        cls.manufacturer = Manufacturer.objects.create(name="BMW Germany")
        cls.car = Car.objects.create(model="X5", manufacturer=cls.manufacturer)
        cls.driver = Driver.objects.create(username="ivan",
                                           license_number="TES12345")

    def test_driver_list_view_requires_login(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_driver_list_view_authenticated(self):
        self.client.login(username="alex", password="12345")
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ivan")

    def test_car_list_search(self):
        self.client.login(username="alex", password="12345")
        response = self.client.get(reverse("taxi:car-list"), {"search": "X5"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "X5")
        self.assertNotContains(response, "A6")
