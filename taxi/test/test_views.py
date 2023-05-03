from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver


class CarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tset",
            password="test12345",
        )

        self.client.force_login(self.user)

    def test_endpoint_car_list_should_work_correct(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )

        Car.objects.create(
            model="test model",
            manufacturer=manufacturer,
        )

        response = self.client.get(reverse("taxi:car-list"))
        cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertEqual(list(response.context["car_list"]), list(cars))

    def test_endpoint_car_detail_should_display_right_car(self):
        manufacturer = Manufacturer.objects.create(
            name="test",
            country="test_country"
        )

        car = Car.objects.create(
            id=55,
            model="test",
            manufacturer=manufacturer,
        )

        response = self.client.get(reverse(
            "taxi:car-detail",
            kwargs={"pk": 55})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")
        self.assertEqual(response.context["car"], car)


class DriverTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="tset",
            password="test12345",
        )

        self.client.force_login(user)

    def test_endpoint_driver_list_should_work_correct(self):
        get_user_model().objects.create_user(
            username="tset1",
            license_number="test12345",
            password="test12345"
        )

        response = self.client.get(reverse("taxi:driver-list"))
        drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertEqual(list(response.context["driver_list"]), list(drivers))

    def test_endpoint_driver_detail_should_display_right_car(self):
        driver = get_user_model().objects.create_user(
            id="55",
            username="tset1",
            license_number="test12345",
            password="test12345"
        )

        response = self.client.get(reverse(
            "taxi:driver-detail",
            kwargs={"pk": 55})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")
        self.assertEqual(response.context["driver"], driver)


class ManufacturerTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            username="tset",
            password="test12345",
        )

        self.client.force_login(user)

    def test_endpoint_manufacturer_list_should_work_correct(self):
        Manufacturer.objects.create(name="test", country="test_county")
        manufacturers = Manufacturer.objects.all()
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
