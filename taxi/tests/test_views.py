from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


class ViewsTest(TestCase):

    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="driver1",
            password="12345",
            license_number="DDD33333"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )
        self.client.login(
            username="driver1",
            password="12345"
        )

    def test_driver_list_view(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/driver_list.html"
        )

    def test_driver_search(self):
        url = reverse("taxi:driver-list") + "?username=driver"
        response = self.client.get(url)
        drivers = response.context["driver_list"]
        self.assertIn(self.driver, drivers)

    def test_car_search(self):
        url = reverse("taxi:car-list") + "?model=Cor"
        response = self.client.get(url)
        cars = response.context["car_list"]
        self.assertIn(self.car, cars)

    def test_manufacturer_search(self):
        url = reverse("taxi:manufacturer-list") + "?name=Toy"
        response = self.client.get(url)
        manufacturers = response.context["manufacturer_list"]
        self.assertIn(self.manufacturer, manufacturers)
