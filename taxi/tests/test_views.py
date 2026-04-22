from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="ZAZ",
            country="Ukraine",
        )
        Manufacturer.objects.create(
            name="Citroen",
            country="France",
        )
        res = self.client.get(MANUFACTURER_URL)
        self.assertEqual(res.status_code, 200)
        manufacturer = Manufacturer.objects.all()
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturer),
        )
        self.assertTemplateUsed(
            res, "taxi/manufacturer_list.html"
        )

    def test_filtered_manufacturers(self):
        Manufacturer.objects.create(
            name="ZAZ",
            country="Ukraine",
        )
        Manufacturer.objects.create(
            name="Citroen",
            country="France",
        )
        res = self.client.get(MANUFACTURER_URL + "?name=zaz")
        manufacturer = Manufacturer.objects.filter(name__icontains="ZAZ")
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(
            res, "taxi/manufacturer_list.html"
        )
        self.assertTrue("search_form" in res.context)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturer),
        )

    def test_retrieve_cars(self):
        driver = get_user_model().objects.create_user(
            username="test1",
            password="test123",
            first_name="Test first name",
            last_name="Test last name",
            license_number="test_license_number",
        )
        manufacturer = Manufacturer.objects.create(
            name="ZAZ",
            country="Ukraine",
        )
        car = Car.objects.create(
            model="test model",
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)
        res = self.client.get(CAR_URL)
        self.assertEqual(res.status_code, 200)
        car = Car.objects.all()
        self.assertEqual(
            list(res.context["car_list"]),
            list(car),
        )
        self.assertTemplateUsed(
            res, "taxi/car_list.html"
        )

    def test_filtered_cars(self):
        driver = get_user_model().objects.create_user(
            username="test1",
            password="test123",
            first_name="Test first name",
            last_name="Test last name",
            license_number="test_license_number",
        )
        manufacturer = Manufacturer.objects.create(
            name="ZAZ",
            country="Ukraine",
        )
        car = Car.objects.create(
            model="Toyota",
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)
        Car.objects.create(
            model="Volvo",
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)
        res = self.client.get(CAR_URL + "?model=volvo")
        self.assertEqual(res.status_code, 200)
        car = Car.objects.filter(model__icontains="volvo")
        self.assertEqual(
            list(res.context["car_list"]),
            list(car),
        )
        self.assertTrue("search_form" in res.context)
        self.assertTemplateUsed(
            res, "taxi/car_list.html"
        )

    def test_filtered_drivers(self):
        get_user_model().objects.create_user(
            username="test_driver",
            password="test123",
            first_name="Test first name",
            last_name="Test last name",
            license_number="test_license_number1",
        )
        get_user_model().objects.create_user(
            username="test_user",
            password="test123",
            first_name="Test first name",
            last_name="Test last name",
            license_number="test_license_number2",
        )
        res = self.client.get(DRIVER_URL + "?username=driver")
        self.assertEqual(res.status_code, 200)
        driver = get_user_model().objects.filter(username__icontains="driver")
        self.assertEqual(
            list(res.context["driver_list"]),
            list(driver),
        )
        self.assertTrue("search_form" in res.context)
        self.assertTemplateUsed(
            res, "taxi/driver_list.html"
        )