from django.test import SimpleTestCase
from django.urls import resolve, reverse

from taxi.views import CarListView, DriverListView, ManufacturerListView


class PrivateUrlTests(SimpleTestCase):

    def test_manufacturer_list_url_str_and_resolve(self):
        url = reverse("taxi:manufacturer-list")

        self.assertEqual(str(url), "/manufacturers/")

        self.assertEqual(resolve(
            str(url)).func.view_class,
            ManufacturerListView
        )

    def test_car_list_url_str_and_resolve(self):
        url = reverse("taxi:car-list")

        self.assertEqual(str(url), "/cars/")
        self.assertEqual(resolve(str(url)).func.view_class, CarListView)

    def test_driver_list_url_str_and_resolve(self):
        url = reverse("taxi:driver-list")

        self.assertEqual(str(url), "/drivers/")
        self.assertEqual(resolve(str(url)).func.view_class, DriverListView)
