from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.forms import DriverSearchForm
from taxi.models import Manufacturer, Driver, Car

manufacturer_url = reverse("taxi:manufacturer-list")
driver_url = reverse("taxi:driver-list")
car_url = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(manufacturer_url)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testusername",
            first_name="testfirstname",
            last_name="testlastname",
            password="testpass"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="Volvo",
            country="Sweden"
        )
        Manufacturer.objects.create(
            name="Opel",
            country="Germany"
        )
        response = self.client.get(manufacturer_url)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicDriverTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testusername",
            first_name="testfirstname",
            last_name="testlastname",
            password="testpass"
        )
        self.client.force_login(self.user)
        self.driver1 = Driver.objects.create(username="user1",
                                             license_number="ANJ12312"
                                             )
        self.driver2 = Driver.objects.create(username="user2",
                                             license_number="ANJ12212"
                                             )
        self.driver3 = Driver.objects.create(username="another_user",
                                             license_number="ANJ02312"
                                             )

        self.driver1 = Driver.objects.create(username="test1",
                                             first_name="test1",
                                             last_name="test1",
                                             license_number="ANJ12112"
                                             )
        self.driver1 = Driver.objects.create(username="test3",
                                             first_name="test3",
                                             last_name="test3",
                                             license_number="AMJ12212"
                                             )
        self.driver1 = Driver.objects.create(username="test4",
                                             first_name="test4",
                                             last_name="test4",
                                             license_number="ANJ02392"
                                             )

    def test_search_with_results(self):
        url = reverse("taxi:driver-list") + "?username=user1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "user1")
        self.assertNotContains(response, "user2")

    def test_search_with_no_results(self):
        url = reverse("taxi:driver-list") + "?username=nonexistent_user"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "user1")
        self.assertNotContains(response, "user2")
        self.assertNotContains(response, "another_user")

    def test_search_form_initial(self):
        response = self.client.get(driver_url)
        self.assertEqual(response.status_code, 200)
        search_form = response.context["search_form"]
        self.assertIsInstance(search_form, DriverSearchForm)
        self.assertEqual(search_form.initial["username"], "")

    def test_login_required(self):
        res = self.client.get(driver_url)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testusername",
            first_name="testfirstname",
            last_name="testlastname",
            password="testpass"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        Driver.objects.create_user(
            username="test",
            first_name="test",
            last_name="test",
            license_number="ANJ12311"
        )
        Driver.objects.create_user(
            username="test1",
            first_name="test1",
            last_name="test1",
            license_number="ANJ12312"
        )
        response = self.client.get(driver_url)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class PublicCarTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(car_url)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testusername",
            first_name="testfirstname",
            last_name="testlastname",
            password="testpass"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer2",
            country="TestCountry"
        )
        self.driver1 = Driver.objects.create(
            license_number="ABC15345",
            username="Driver1"
        )
        self.driver2 = Driver.objects.create(
            license_number="ABC42346",
            username="Driver2"
        )

    def test_retrieve_drivers(self):
        Car.objects.create(model="TestModel", manufacturer=self.manufacturer)
        Car.objects.create(model="TestModel1", manufacturer=self.manufacturer)
        response = self.client.get(car_url)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")
