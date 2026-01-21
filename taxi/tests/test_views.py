from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import CarSearchForm
from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Skoda")
        Manufacturer.objects.create(name="Audi")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class ManufacturersSearchTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.login(username="testuser", password="password")

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Honda",
            country="Japan"
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

    def test_search_manufacturer(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list"
        ), {"name": "Toyota"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["manufacturer_list"], [
            self.manufacturer1
        ])

    def test_search_no_result(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list"), {"name": "Opel"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"], []
        )


class CarSearchTest(TestCase):
    def setUp(self):
        user = get_user_model()
        self.user = user.objects.create_user(
            username="testuser",
            password="password"
        )
        self.client.login(username="testuser", password="password")
        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Honda", country="Japan"
        )

        self.car1 = Car.objects.create(
            model="Corolla", manufacturer=self.manufacturer1,
        )
        self.car2 = Car.objects.create(
            model="Civic", manufacturer=self.manufacturer2,
        )
        self.car3 = Car.objects.create(
            model="Accord", manufacturer=self.manufacturer2
        )

    def test_search_car_by_model(self):
        """
        TEST SEARCHING FOR A CAR BY MODEL
        """
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Civic"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car2.model)
        self.assertNotContains(response, self.car1.model)
        self.assertNotContains(response, self.car3.model)

    def test_search_no_result(self):
        """
        TEST SEARCHING FOR A CAR WITH NO RESULT
        """
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["search_form"], CarSearchForm)
        self.assertContains(response, 'placeholder="Search by model"')
