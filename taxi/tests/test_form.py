from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class SearchFormTests(TestCase):
    def setUp(self):
        user = Driver.objects.create_user(
            username="test",
            password="test123",
            license_number="ABC12345",
        )
        self.client.force_login(user)

    def test_search_form_in_manufacturer_list(self):
        Manufacturer.objects.create(
            name="test",
            country="test_country",
        )
        manufacturer = Manufacturer.objects.filter(name__icontains="t")

        url = reverse("taxi:manufacturer-list") + "?name=t"
        response = self.client.get(url)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer),
        )

    def test_search_form_in_driver_list(self):
        driver = Driver.objects.filter(username__icontains="t")

        url = reverse("taxi:driver-list") + "?username=t"
        response = self.client.get(url)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver),
        )

    def test_search_form_in_car_list(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country",
        )
        Car.objects.create(
            model="test",
            manufacturer=manufacturer,
        )
        car = Car.objects.filter(model__icontains="t")

        url = reverse("taxi:car-list") + "?model=t"
        response = self.client.get(url)
        self.assertEqual(
            list(response.context["car_list"]),
            list(car),
        )
