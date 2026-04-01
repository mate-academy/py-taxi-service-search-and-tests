from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class ManufacturerListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.force_login(user)

    @classmethod
    def setUpTestData(cls):
        number_of_manufacturers = 13
        from taxi.models import Manufacturer

        for manu_id in range(number_of_manufacturers):
            Manufacturer.objects.create(
                name=f"1_Manufacturer_{manu_id}",
                country=f"1_Country_{manu_id}",
            )

    def test_manufacturer_list_view_url_exists(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_list_view_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "1_Manufacturer_0"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1_Manufacturer_0")

    def test_manufacturer_list_view_search_no_results(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "xxx"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "There are no manufacturers in the service.",
            msg_prefix="Should display no results message when name does not match any manufacturer",
        )


class CarListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.force_login(user)

    @classmethod
    def setUpTestData(cls):
        from taxi.models import Car, Manufacturer

        manufacturer = Manufacturer.objects.create(
            name="CarManu", country="US"
        )
        for car_id in range(11):
            Car.objects.create(
                model=f"TestModel_{car_id}", manufacturer=manufacturer
            )

    def test_car_list_view_url_exists(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

    def test_car_list_view_search(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "TestModel_0"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TestModel_0")

    def test_car_list_view_search_no_results(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "xxx"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "There are no cars in the service.",
            msg_prefix="Should display no results message when model does not match any car",
        )


class DriverListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        user = get_user_model().objects.create_user(
            username="testuser", password="testpass", license_number="ABC12345"
        )
        self.client.force_login(user)

    @classmethod
    def setUpTestData(cls):
        from taxi.models import Driver

        for driver_id in range(9):
            Driver.objects.create(
                username=f"testdriver_{driver_id}",
                password="pass",
                license_number=f"ABCDE{driver_id:03d}",
            )

    def test_driver_list_view_url_exists(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)

    def test_driver_list_view_search(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "testdriver_0"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testdriver_0")

    def test_driver_list_view_search_no_results(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "xxx"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "There are no drivers in the service.",
            msg_prefix="Should display no results message when username does not match any driver",
        )
