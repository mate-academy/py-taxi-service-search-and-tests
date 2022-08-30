from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class ManufacturerListViewTests(TestCase):
    URL_MANUFACTURERS_LIST = reverse("taxi:manufacturer-list")

    def setUp(self):
        Manufacturer.objects.create(
            name=f"name_test",
            country=f"country_test",
        )

        driver = get_user_model().objects.create_user(
            license_number="QWS22113",
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
            password="test_password"
        )
        self.client.force_login(driver)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.URL_MANUFACTURERS_LIST)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.URL_MANUFACTURERS_LIST)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_manufacturer(self):
        response = self.client.get(self.URL_MANUFACTURERS_LIST)
        manufacturer_list = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer_list))


class CarListViewTests(TestCase):
    URL_CAR_LIST = reverse("taxi:car-list")

    def setUp(self):
        manufacturer = Manufacturer.objects.create(
            name=f"name_test",
            country=f"country_test",
        )
        car = Car.objects.create(
            model=f"model_test",
            manufacturer=manufacturer
        )
        driver = get_user_model().objects.create_user(
            license_number="QWS22113",
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
            password="test_password"
        )
        car.drivers.add(driver)

        self.client.force_login(driver)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.URL_CAR_LIST)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_car(self):
        response = self.client.get(self.URL_CAR_LIST)
        car_list = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(car_list))


class DriverListViewTests(TestCase):
    URL_DRIVER_LIST = reverse("taxi:driver-list")

    def setUp(self):
        driver = get_user_model().objects.create_user(
            license_number="QWS22113",
            username="test_username",
            first_name="test_first_name",
            last_name="test_last_name",
            password="test_password"
        )
        self.client.force_login(driver)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.URL_DRIVER_LIST)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_car(self):
        response = self.client.get(self.URL_DRIVER_LIST)
        driver_list = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(driver_list))
