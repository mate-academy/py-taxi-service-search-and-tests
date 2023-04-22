from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class ResponseNonLoggedTest(TestCase):
    def test_manufacturers_list(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_drivers_list(self):
        res = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_drivers_detail(self):
        res = self.client.get(reverse("taxi:driver-detail", kwargs={"pk": 1}))
        self.assertNotEqual(res.status_code, 200)

    def test_cars_list(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertNotEqual(res.status_code, 200)

    def test_cars_detail(self):
        res = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": 1})
        )
        self.assertNotEqual(res.status_code, 200)


class ResponseLoggedTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.client = Client()
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(name="Daewoo Lanos",
                                                        country="Ukraine")
        Car.objects.create(model="test", manufacturer=self.manufacturer)

    def test_retrieve_manufacturers(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_manufacturers_with_search(self):
        url_with_search = reverse("taxi:manufacturer-list") + "?name=Lanos"
        response = self.client.get(url_with_search)
        manufacturers = Manufacturer.objects.filter(name__icontains="Lanos")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_get_drivers_list(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_get_drivers_list_with_search(self):
        url_with_search = reverse("taxi:driver-list") + "?username=test"
        response = self.client.get(url_with_search)
        drivers = Driver.objects.filter(username__icontains="test")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_get_driverds_detail(self):
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_get_cars_list(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_get_cars_list_with_search(self):
        url_with_search = reverse("taxi:car-list") + "?model=test"
        response = self.client.get(url_with_search)
        cars = Car.objects.filter(model__icontains="test")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_get_cars_detail(self):
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": 1})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")
