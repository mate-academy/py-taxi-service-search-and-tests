from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Driver, Car, Manufacturer


User = get_user_model()


class SearchViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser",
                                            password="12345")

        cls.manufacturer1 = Manufacturer.objects.create(name="BMW Germany")
        cls.manufacturer2 = Manufacturer.objects.create(name="Audi Germany")

        cls.car1 = Car.objects.create(model="X5",
                                      manufacturer=cls.manufacturer1)
        cls.car2 = Car.objects.create(model="A6",
                                      manufacturer=cls.manufacturer2)

        cls.driver1 = Driver.objects.create(username="ivan",
                                            license_number="TES12345")
        cls.driver2 = Driver.objects.create(username="petro",
                                            license_number="TES12346")

    def setUp(self):
        self.client.login(username="testuser", password="12345")

    def test_driver_search_view(self):
        response = self.client.get(reverse("taxi:driver-list"),
                                   {"search": "ivan"})
        self.assertEqual(response.status_code, 200)
        drivers = response.context["driver_list"]
        self.assertIn(self.driver1, drivers)
        self.assertNotIn(self.driver2, drivers)

    def test_car_search_view(self):
        response = self.client.get(reverse("taxi:car-list"), {"search": "X5"})
        self.assertEqual(response.status_code, 200)
        cars = response.context["car_list"]
        self.assertIn(self.car1, cars)
        self.assertNotIn(self.car2, cars)

    def test_manufacturer_search_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"),
                                   {"search": "BMW"})
        self.assertEqual(response.status_code, 200)
        manufacturers = response.context["manufacturer_list"]
        self.assertIn(self.manufacturer1, manufacturers)
        self.assertNotIn(self.manufacturer2, manufacturers)
