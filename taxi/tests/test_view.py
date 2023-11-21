from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer

HOME_PAGE = reverse("taxi:index")


class IndexViewTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create(
            username="testuser",
            password="testpass123",
            license_number="ASJ37397"
        )
        self.driver2 = get_user_model().objects.create(
            username="testuser2",
            password="testpass1234",
            license_number="ASJ37394"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer"
        )
        self.car = Car.objects.create(
            model="Test Car",
            manufacturer=self.manufacturer,
        )
        self.client.force_login(self.driver)

    def test_public_index_view(self):
        self.client.logout()
        response = self.client.get(HOME_PAGE)
        redirected_url = "/accounts/login/?next=/"
        self.assertEqual(response.url, redirected_url)
        self.assertEqual(response.status_code, 302)

    def test_content_in_home_page(self):
        response = self.client.get(HOME_PAGE)
        response = self.client.get(HOME_PAGE)

        self.assertEqual(response.context["num_drivers"], 2)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_manufacturers"], 1)
        self.assertEqual(response.context["num_visits"], 2)

    def test_index_view_statis_code(self):
        response = self.client.get(HOME_PAGE)
        self.assertEqual(response.status_code, 200)


class ManufacturerPublicViewTest(TestCase):
    def test_manufacturer_list_redirect(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_manufacturer_create_redirect(self):
        url = reverse("taxi:manufacturer-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_manufacturer_update_redirect(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Testmanu",
            country="Uk"
        )
        url = "/manufacturers/1/update/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_manufacturer_delete_redirect(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Testmanu",
            country="Uk"
        )
        url = "/manufacturers/1/delete/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class ManufacturerPrivateViewTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create(
            username="testuser",
            password="testpass123",
            license_number="ASJ37397"
        )
        self.client.force_login(self.driver)

    def test_manufacturer_open_list_page(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_create_page(self):
        url = reverse("taxi:manufacturer-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        Manufacturer.objects.create(name="1", country="1")
        manufacturers = Manufacturer.objects.count()
        self.assertEqual(manufacturers, 1)

    def test_manufacturer_open_update_page(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Testmanu",
            country="Uk"
        )
        url = "/manufacturers/1/update/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_open_delete_page(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Testmanu",
            country="Uk"
        )
        url = "/manufacturers/1/delete/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delete manufacturer?")


class CarPublicViewTest(TestCase):
    def test_car_list_redirect(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_car_create_redirect(self):
        url = reverse("taxi:car-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class CarPrivateViewTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create(
            username="testdriver",
            password="driverpass123",
            license_number="ASJ37397"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="yest",
            country="Ukraine"
        )
        self.car = Car.objects.create(
            model="Audi",
            manufacturer=self.manufacturer
        )
        self.client.force_login(self.driver)

    def test_car_list(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        name = Car.objects.first()
        self.assertContains(response, name)

    def test_car_create(self):
        url = reverse("taxi:manufacturer-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        Car.objects.create(model="1", manufacturer=self.manufacturer)
        Car.objects.create(model="2", manufacturer=self.manufacturer)
        cars = Car.objects.count()
        self.assertEqual(cars, 3)

    def test_car_open_update_page(self):
        url = "/cars/1/update/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_open_delete_page(self):
        url = "/cars/1/delete/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delete car?")


class DriverPublicViewTest(TestCase):
    def test_driver_list_redirect(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_driver_create_redirect(self):
        url = reverse("taxi:driver-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


class DriverPrivateViewTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create(
            username="testdriver",
            password="driverpass123",
            license_number="ASJ37397"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="yest",
            country="Ukraine"
        )
        self.client.force_login(self.driver)

    def test_open_driver_list(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        name = get_user_model().objects.first().username
        self.assertContains(response, name)

    def test_driver_create(self):
        url = reverse("taxi:driver-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        get_user_model().objects.create(
            username="driver2",
            password="driver2123",
            license_number="AEJ37397"
        )
        drivers = get_user_model().objects.count()
        self.assertEqual(drivers, 2)

    def test_driver_open_update_page(self):
        url = "/drivers/1/update/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_driver_open_delete_page(self):
        url = "/drivers/1/delete/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delete driver?")
