from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm, CarSearchForm, DriverSearchForm
from taxi.models import Manufacturer, Car, Driver

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
CARS_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerListTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerListTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="test", password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        Manufacturer.objects.create(name="Suzuki", country="Japan")
        Manufacturer.objects.create(name="Volvo", country="Sweden")

        resp = self.client.get(MANUFACTURERS_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            list(resp.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(resp, "taxi/manufacturer_list.html")

    def test_get_context_data(self):
        resp = self.client.get(MANUFACTURERS_URL)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("search_form", resp.context)
        self.assertIsInstance(
            resp.context["search_form"], ManufacturerSearchForm
        )

    def test_get_queryset(self):
        Manufacturer.objects.create(name="Suzuki", country="Japan")
        Manufacturer.objects.create(name="Volvo", country="Sweden")

        resp = self.client.get(MANUFACTURERS_URL)

        self.assertEqual(resp.status_code, 200)
        self.assertQuerysetEqual(
            list(
                resp.context["manufacturer_list"]
            ), list(Manufacturer.objects.all())
        )
        self.assertTemplateUsed(resp, "taxi/manufacturer_list.html")

    def test_queryset_with_filtered_data(self):
        resp = self.client.get(MANUFACTURERS_URL, {"name": "Suzuki"})
        self.assertEqual(resp.status_code, 200)

        filtered_queryset = Manufacturer.objects.filter(name__icontains="Suz")

        self.assertEqual(
            list(resp.context["manufacturer_list"]), list(filtered_queryset)
        )


class PublicCarListTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(CARS_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateCarListTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="test", password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_car(self):
        manufacturer1 = Manufacturer.objects.create(
            name="Suzuki",
            country="Japan"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Volvo",
            country="Sweden"
        )
        Car.objects.create(model="Jimhny", manufacturer=manufacturer1)
        Car.objects.create(model="C90", manufacturer=manufacturer2)

        resp = self.client.get(CARS_URL)

        cars = Car.objects.all()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(list(resp.context["car_list"]), list(cars))
        self.assertTemplateUsed(resp, "taxi/car_list.html")

    def test_get_context_data(self):
        resp = self.client.get(CARS_URL)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("search_form", resp.context)
        self.assertIsInstance(resp.context["search_form"], CarSearchForm)

    def test_get_queryset(self):
        manufacturer1 = Manufacturer.objects.create(
            name="Suzuki", country="Japan"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Volvo", country="Sweden"
        )
        Car.objects.create(model="Jihmny", manufacturer=manufacturer1)
        Car.objects.create(model="XC90", manufacturer=manufacturer2)

        resp = self.client.get(CARS_URL)

        self.assertEqual(resp.status_code, 200)
        self.assertQuerysetEqual(
            list(resp.context["car_list"]), list(Car.objects.all())
        )
        self.assertTemplateUsed(resp, "taxi/car_list.html")

    def test_queryset_with_filtered_data(self):
        manufacturer1 = Manufacturer.objects.create(
            name="Suzuki", country="Japan"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Volvo", country="Sweden"
        )
        Car.objects.create(model="Jihmny", manufacturer=manufacturer1)
        Car.objects.create(model="XC90", manufacturer=manufacturer2)

        resp = self.client.get(CARS_URL, {"model": "Jimhny"})
        self.assertEqual(resp.status_code, 200)

        filtered_queryset = Car.objects.filter(model__icontains="Jim")

        self.assertEqual(
            list(resp.context["car_list"]), list(filtered_queryset)
        )


class PublicDriverListTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(DRIVER_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateDriverListTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="test", password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create(
            username="JohnWick", password="test1234", license_number="ABC12345"
        )
        Driver.objects.create(
            username="MichaelShumacher",
            password="test1234",
            license_number="ABC12346"
        )

        resp = self.client.get(DRIVER_URL)

        drivers = Driver.objects.all()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(list(resp.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(resp, "taxi/driver_list.html")

    def test_get_context_data(self):
        resp = self.client.get(DRIVER_URL)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("search_form", resp.context)
        self.assertIsInstance(resp.context["search_form"], DriverSearchForm)

    def test_get_queryset(self):
        Driver.objects.create(
            username="JohnWick", password="test1234", license_number="ABC12345"
        )
        Driver.objects.create(
            username="MichaelShumacher",
            password="test1234",
            license_number="ABC12346"
        )

        resp = self.client.get(DRIVER_URL)

        self.assertEqual(resp.status_code, 200)
        self.assertQuerysetEqual(
            list(resp.context["driver_list"]), list(Driver.objects.all())
        )
        self.assertTemplateUsed(resp, "taxi/driver_list.html")

    def test_queryset_with_filtered_data(self):
        Driver.objects.create(
            username="JohnWick", password="test1234", license_number="ABC12345"
        )
        Driver.objects.create(
            username="MichaelShumacher",
            password="test1234",
            license_number="ABC12346"
        )
        resp = self.client.get(DRIVER_URL, {"username": "MichaelShumacher"})
        self.assertEqual(resp.status_code, 200)

        filtered_queryset = Driver.objects.filter(username__icontains="Shuma")

        self.assertEqual(
            list(resp.context["driver_list"]), list(filtered_queryset)
        )
