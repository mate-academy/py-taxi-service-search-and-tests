from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVERS_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):

    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user",
            password="qwertyui"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Honda Motor Corporation")
        Manufacturer.objects.create(name="Dodge Brothers")
        res = self.client.get(MANUFACTURER_URL)
        self.assertEquals(res.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEquals(
            list(res.context["manufacturer_list"]),
            list(manufacturer),
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_search_manufacturer_by_name(self):
        Manufacturer.objects.create(name="Dodge Brothers")
        searched_name = "Dodge Brothers"
        response = self.client.get(
            MANUFACTURER_URL,
            {"name": searched_name}
        )
        self.assertEqual(response.status_code, 200)
        manufacturer_in_context = Manufacturer.objects.filter(
            name__icontains=searched_name
        )
        self.assertQuerysetEqual(
            response.context["manufacturer_list"], manufacturer_in_context
        )


class PublicCarTest(TestCase):

    def test_car_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Roman",
            password="qwertyui",
            license_number="REO33658"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer = Manufacturer.objects.create(name="test2")
        Car.objects.create(
            model="test2",
            manufacturer=manufacturer
        )

        response = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_search_by_name(self) -> None:
        manufacturer1 = Manufacturer.objects.create(name="Wrangler Corp")
        Car.objects.create(
            model="Wrangler", manufacturer=manufacturer1
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"model": "Wrangler", "manufacturer": "Wrangler Corp"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Wrangler",
            count=1,
            status_code=200
        )
        self.assertContains(
            response,
            "Wrangler Corp",
            count=1,
            status_code=200
        )

    def test_driver_search(self):
        self.driver1 = get_user_model().objects.create(
            username="romkapomka")
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "romkapomka"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "romkapomka")
        self.assertNotContains(response, "pomkaromka")
