from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Driver, Car


MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrive_manufacturer(self):
        Manufacturer.objects.create(name="test1", country="test_contry_1")
        Manufacturer.objects.create(name="test2", country="test_contry_2")
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrive_driver(self):
        Driver.objects.create_user(
            username="Mike_1",
            password="test123",
            license_number="ADM56984"
        )
        Driver.objects.create_user(
            username="Mike_2",
            password="test123",
            license_number="ADM56986"
        )
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

    def test_retrive_car(self):
        manufacturer = Manufacturer.objects.create(
            name="test1",
            country="test_contry_1"
        )
        driver = Driver.objects.create(
            username="Test",
            password="test123",
            first_name="test_first",
            last_name="test_second",
            license_number="ADM56986"
        )
        car = Car.objects.create(
            model="Test",
            manufacturer=manufacturer,
        )
        car.drivers.add(driver)
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        car = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(car)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class SearchFeatureTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.driver1 = get_user_model().objects.create_user(
            username="john_doe",
            password="test12345",
            license_number="ABC12345"
        )
        self.driver2 = get_user_model().objects.create_user(
            username="alice_smith",
            password="test12345",
            license_number="XYZ67890"
        )

        self.manufacturer1 = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )

        self.car1 = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="X5",
            manufacturer=self.manufacturer2
        )

        self.car1.drivers.add(self.driver1)
        self.car2.drivers.add(self.driver2)

        self.client.force_login(self.driver1)

    def test_driver_search_returns_correct_results(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=john"
        )
        self.assertContains(response, "john_doe")
        self.assertNotContains(response, "alice_smith")

    def test_driver_search_empty_returns_all(self):
        response = self.client.get(reverse("taxi:driver-list") + "?username=")
        self.assertContains(response, "john_doe")
        self.assertContains(response, "alice_smith")

    def test_car_search_returns_correct_results(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=X5")
        self.assertContains(response, "X5")
        self.assertNotContains(response, "Camry")

    def test_car_search_empty_returns_all(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=")
        self.assertContains(response, "X5")
        self.assertContains(response, "Camry")

    def test_manufacturer_search_returns_correct_results(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=BMW"
        )
        self.assertContains(response, "BMW")
        self.assertNotContains(response, "Toyota")

    def test_manufacturer_search_empty_returns_all(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name="
        )
        self.assertContains(response, "BMW")
        self.assertContains(response, "Toyota")

    def test_search_form_in_context(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertIn("search_form", response.context)

        response = self.client.get(reverse("taxi:car-list"))
        self.assertIn("search_form", response.context)

        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertIn("search_form", response.context)
