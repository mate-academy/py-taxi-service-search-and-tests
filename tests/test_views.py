from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        """Test that Manufacturer list is not displayed when
        we are not logged in"""
        response = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="user", password="cde123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer(self):
        """Test displaying Manufacturer list when we logged in
        and views using correct template"""
        Manufacturer.objects.create(name="test name", country="test country")
        Manufacturer.objects.create(name="test name1", country="test country1")
        response = self.client.get(MANUFACTURERS_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer_by_name(self):
        """Test that we can find Manufacturer by name"""
        Manufacturer.objects.create(name="test name", country="test country")
        search_name = "test name"
        response = self.client.get(MANUFACTURERS_URL, {"name": search_name})
        context_manufacturer = Manufacturer.objects.filter(
            name__icontains=search_name
        )

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"], context_manufacturer
        )


class PublicDriverTest(TestCase):
    def test_login_required(self):
        """Test that Driver list is not displayed where
        we are not logged in"""
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.driver = get_user_model().objects.create_user(
            username="driver",
            password="driver12345",
            license_number="ABC12345"
        )
        self.client.force_login(self.driver)

    def test_retrieve_driver(self):
        """Test displaying Driver list when we logged in
        and views using correct template"""
        Driver.objects.create(username="test")
        response = self.client.get(DRIVER_URL)
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_driver_by_name(self):
        """Test that we can find Driver by name"""
        Driver.objects.create(username="test")
        search_name = "test"
        response = self.client.get(DRIVER_URL, {"username": search_name})
        context_driver = Driver.objects.filter(username__icontains=search_name)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["driver_list"],
            context_driver,
        )


class PublicCarTest(TestCase):
    def test_login_required(self):
        """Test that Car list is not displayed where
        we are not logged in"""
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test", "qaz123", "QWE12345"
        )
        self.client.force_login(self.user)

    def test_retrieve_driver(self):
        """Test displaying Car list when we logged in
        and views using correct template"""
        manufacturer = Manufacturer.objects.create(name="test name")
        Car.objects.create(model="test model", manufacturer=manufacturer)
        response = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")
