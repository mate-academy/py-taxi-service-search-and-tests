from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car
from taxi.forms import DriverSearchForm, ManufacturerSearchForm, CarSearchForm

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")


class PublicTest(TestCase):
    """Test the publicly available pages"""
    def test_login_required_for_manufacturer_list(self) -> None:
        """Test the publicly available manufacturer pages"""
        res = self.client.get(MANUFACTURER_URL)

        self.assertEqual(res.status_code, 302)

    def test_login_required_for_driver_list(self) -> None:
        """Test the publicly available driver pages"""
        res = self.client.get(DRIVER_URL)

        self.assertEqual(res.status_code, 302)

    def test_login_required_for_car_list(self) -> None:
        """Test the publicly available car pages"""
        res = self.client.get(CAR_URL)

        self.assertEqual(res.status_code, 302)


class PrivateTest(TestCase):
    """Test the authorized user has access to pages"""
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="password",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self) -> None:
        """Test the authorized user has access to manufacturer pages"""
        Manufacturer.objects.create(name="Renault", country="France")
        Manufacturer.objects.create(name="Peugeot", country="France")
        res = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(
            res.context["manufacturer_list"],
            manufacturers,
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_retrieve_driver_list(self) -> None:
        """Test the authorized user has access to driver pages"""
        Driver.objects.create(username="user1", license_number="ABC12345")
        Driver.objects.create(username="user2", license_number="ABC54321")
        res = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(
            res.context["driver_list"], drivers, ordered=False
        )
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_retrieve_car_list(self) -> None:
        """Test the authorized user has access to car pages"""
        manufacturer = Manufacturer.objects.create(
            name="Renault", country="France"
        )

        Car.objects.create(model="Scenic", manufacturer=manufacturer)
        Car.objects.create(model="Logan", manufacturer=manufacturer)

        res = self.client.get(CAR_URL)
        cars = Car.objects.all()
        self.assertEqual(res.status_code, 200)
        self.assertQuerysetEqual(res.context["car_list"], cars, ordered=False)
        self.assertTemplateUsed(res, "taxi/car_list.html")


class SearchTests(TestCase):
    """Tests search bars functionality"""
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="password",
        )
        self.client.force_login(self.user)

    def test_search_driver_by_username(self) -> None:
        Driver.objects.create(username="user1", license_number="ABC12345")
        Driver.objects.create(username="user2", license_number="ABC54321")

        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "user2"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context["search_form"], DriverSearchForm
        )
        self.assertQuerysetEqual(
            response.context["driver_list"],
            Driver.objects.filter(username__icontains="user2"),
        )

    def test_search_car_by_model(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Renault", country="France"
        )
        Car.objects.create(model="Scenic", manufacturer=manufacturer)
        Car.objects.create(model="Logan", manufacturer=manufacturer)

        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Scenic"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["search_form"], CarSearchForm)
        self.assertQuerysetEqual(
            response.context["car_list"],
            Car.objects.filter(model__icontains="Scenic"),
        )

    def test_search_manufacturer_by_name(self) -> None:
        Manufacturer.objects.create(name="Renault", country="France")
        Manufacturer.objects.create(name="Peugeot", country="France")

        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Renault"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context["search_form"], ManufacturerSearchForm
        )
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            Manufacturer.objects.filter(name__icontains="Renault"),
        )
