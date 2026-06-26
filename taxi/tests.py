from django.test import TestCase
from django.urls import reverse
from taxi.models import Driver, Manufacturer, Car


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.user = (Driver.objects.
                     create_user(username="dzi", password="qaz12"))

    def test_list_manufacturer(self):
        self.client.login(username="dzi", password="qaz12")
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertContains(response, "Search by name")

    def test_search_manufacturer(self):
        self.client.login(username="dzi", password="qaz12")
        Manufacturer.objects.create(name="BMW", country="Germany")
        response = (self.client.
                    get(reverse("taxi:manufacturer-list") + "?q=BMW"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW")

    def test_search_no_results(self):
        self.client.login(username="dzi", password="qaz12")
        response = (self.client.
                    get(reverse("taxi:manufacturer-list") + "?q=XYZ"))
        self.assertEqual(response.status_code, 200)


class DriverListViewTest(TestCase):
    def setUp(self):
        self.user = (Driver.objects.
                     create_user(username="dzi", password="qaz12"))

    def test_list_driver(self):
        self.client.login(username="dzi", password="qaz12")
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertContains(response, "Search Drivers")

    def test_search_driver(self):
        self.client.login(username="dzi", password="qaz12")
        Driver.objects.create_user(username="Dzik",
                                   password="qaz12",
                                   license_number="QAZ123")
        response = self.client.get(reverse("taxi:driver-list") + "?q=Dzik")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dzik")

    def test_search_no_results(self):
        self.client.login(username="dzi", password="qaz12")
        response = self.client.get(reverse("taxi:driver-list") + "?q=XYZ")
        self.assertEqual(response.status_code, 200)


class CarListViewTest(TestCase):
    def setUp(self):
        self.user = (Driver.objects.
                     create_user(username="dzi", password="qaz12"))

    def test_list_car(self):
        self.client.login(username="dzi", password="qaz12")
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertContains(response, "Search cars")

    def test_search_car(self):
        self.client.login(username="dzi", password="qaz12")
        bmw = Manufacturer.objects.create(name="BMW", country="Germany")
        Car.objects.create(model="szrot", manufacturer=bmw)
        response = self.client.get(reverse("taxi:car-list") + "?q=szrot")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "szrot")

    def test_search_no_results(self):
        self.client.login(username="dzi", password="qaz12")
        response = self.client.get(reverse("taxi:car-list") + "?q=XYZ")
        self.assertEqual(response.status_code, 200)
