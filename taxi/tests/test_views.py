from django.contrib.auth import get_user_model
from django.utils.http import urlencode
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicTests(TestCase):
    def test_login_required(self):
        res_manufacturer = self.client.get(MANUFACTURER_URL)
        res_car = self.client.get(CAR_URL)
        res_driver = self.client.get(DRIVER_URL)

        self.assertNotEqual(res_manufacturer.status_code, 200)
        self.assertNotEqual(res_car.status_code, 200)
        self.assertNotEqual(res_driver.status_code, 200)


class PrivatTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

        manufacturer1 = Manufacturer.objects.create(
            name="test1",
            country="UKR"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="test2",
            country="CAN"
        )
        manufacturer3 = Manufacturer.objects.create(
            name="test3",
            country="USA"
        )

        Car.objects.create(model="test1", manufacturer=manufacturer1)
        Car.objects.create(model="test2", manufacturer=manufacturer1)
        Car.objects.create(model="test3", manufacturer=manufacturer2)
        Car.objects.create(model="test123", manufacturer=manufacturer3)

        get_user_model().objects.create(
            username="test1",
            password="test123",
            license_number="AAA12345"
        )
        get_user_model().objects.create(
            username="test2",
            password="test123",
            license_number="BBB12345"
        )
        get_user_model().objects.create(
            username="test3",
            password="test123",
            license_number="CCC12345"
        )
        get_user_model().objects.create(
            username="test123",
            password="test123",
            license_number="DDD12345"
        )

    def test_retrive_manufacturer_list(self):
        res = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(res, "taxi/manufacturer_list.html")

    def test_filter_manufacturer_list(self):
        filter_value = "3"
        res = self.client.get(
            f'{MANUFACTURER_URL}?{urlencode({"name": filter_value})}'
        )
        manufacturers = Manufacturer.objects.filter(
            name__icontains=filter_value
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_retrive_car_list(self):
        res = self.client.get(CAR_URL)
        cars = Car.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["car_list"]), list(cars))
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_filter_car_list(self):
        filter_value = "1"
        res = self.client.get(
            f'{CAR_URL}?{urlencode({"model": filter_value})}'
        )
        cars = Car.objects.filter(model__icontains=filter_value)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["car_list"]), list(cars))

    def test_retrive_driver_list(self):
        res = self.client.get(DRIVER_URL)
        drivers = get_user_model().objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_filter_driver_list(self):
        filter_value = "2"
        res = self.client.get(
            f'{DRIVER_URL}?{urlencode({"username": filter_value})}'
        )
        drivers = get_user_model().objects.filter(
            username__icontains=filter_value
        )

        self.assertEqual(res.status_code, 200)
        self.assertEqual(list(res.context["driver_list"]), list(drivers))

    def test_create_driver(self):
        form_data = {
            "username": "test4",
            "password1": "test123321",
            "password2": "test123321",
            "first_name": "test_first",
            "last_name": "test_last",
            "license_number": "ABC12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )

        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"]
        )
