from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

CAR_URL = reverse("taxi:car-list")


class PublicCarTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            username="testuser",
            password="<PASSWORD>",
        )
        driver = Driver.objects.create_user(
            username="driver",
            password="<PASSWORD>",
            license_number="AZS12345",
        )
        manufacturer = Manufacturer.objects.create(name="BMW", country="US")
        first_car = Car.objects.create(
            model="Z3",
            manufacturer=manufacturer,
        )
        first_car.drivers.add(driver)
        second_car = Car.objects.create(
            model="X3",
            manufacturer=manufacturer,
        )
        second_car.drivers.add(driver)
        third_car = Car.objects.create(
            model="M3",
            manufacturer=manufacturer,
        )
        third_car.drivers.add(driver)

    def setUp(self):
        self.client.force_login(self.user)

    def test_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_context(self):
        response = self.client.get(CAR_URL)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertIn("search_form", response.context)

    def test_list_car(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Z3")
        self.assertContains(response, "X3")
        self.assertContains(response, "M3")

    def test_car_search_by_model(self):
        response = self.client.get(CAR_URL, {"model": "z"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Z3")
        self.assertNotContains(response, "X3")
        self.assertNotContains(response, "M3")

    def test_car_search_with_no_match(self):
        response = self.client.get(CAR_URL, {"model": "y"})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Z3")
        self.assertNotContains(response, "X3")
        self.assertNotContains(response, "M3")
        self.assertContains(response,
                            "There are no cars in taxi",
                            html=True)
