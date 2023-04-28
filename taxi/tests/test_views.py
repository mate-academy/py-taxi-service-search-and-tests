from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
DRIVERS_URL = reverse("taxi:driver-list")
CARS_URL = reverse("taxi:car-list")
HOME_URL = reverse("taxi:index")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Test1", country="Test1")
        Manufacturer.objects.create(name="Test2", country="Test2")

        response = self.client.get(MANUFACTURERS_URL)
        manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )

    def test_driver_list_login_required(self):
        response = self.client.get(DRIVERS_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_driver_detail_login_required(self):
        url = reverse("taxi:driver-detail", kwargs={"pk": self.user.id})
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        get_user_model().objects.create_user(
            username="Test1",
            password="Test1234",
            license_number="TES1234"
        )
        get_user_model().objects.create_user(
            username="Test2",
            password="Test1234",
            license_number="TES1235"
        )

        response = self.client.get(DRIVERS_URL)
        drivers = get_user_model().objects.prefetch_related("cars")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_driver_detail(self):
        url = reverse("taxi:driver-detail", kwargs={"pk": self.user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_create_driver(self):
        form_data = {
            "username": "Test.1",
            "password1": "Test12345",
            "password2": "Test12345",
            "first_name": "Name",
            "last_name": "Surname",
            "license_number": "TES12345"
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(
            username=form_data["username"]
        )
        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])


class PublicCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )

    def test_car_list_login_required(self):
        response = self.client.get(CARS_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_car_detail_login_required(self):
        manufacturer = Manufacturer.objects.create(
            name="Test1",
            country="Test"
        )
        car = Car.objects.create(
            model="Test1",
            manufacturer=manufacturer
        )
        url = reverse("taxi:car-detail", kwargs={"pk": car.id})
        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test",
            country="test1"
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):

        Car.objects.create(
            model="Test1",
            manufacturer=self.manufacturer
        )
        Car.objects.create(
            model="Test2",
            manufacturer=self.manufacturer
        )

        response = self.client.get(CARS_URL)
        cars = Car.objects.select_related("manufacturer")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_car_detail(self):
        car = Car.objects.create(
            model="Test1",
            manufacturer=self.manufacturer
        )
        url = reverse("taxi:car-detail", kwargs={"pk": car.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")


class PublicHomePageTest(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="Test1",
            password="test1234"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test2",
            country="Country"
        )
        self.car = Car.objects.create(
            model="Test3",
            manufacturer=self.manufacturer
        )

    def test_home_page_list_login_required(self):
        response = self.client.get(HOME_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateHomePageTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )

        self.client.force_login(self.user)

    def test_retrieve_home_page_information(self):
        manufacturer = Manufacturer.objects.create(
            name="test", country="test1"
        )
        Car.objects.create(model="Test3", manufacturer=manufacturer)
        Car.objects.create(model="Test", manufacturer=manufacturer)
        get_user_model().objects.create_user(
            username="Test1",
            password="test12345",
            license_number="TES12345"
        )

        num_drivers = get_user_model().objects.count()
        num_manufacturers = Manufacturer.objects.count()
        num_cars = Car.objects.count()

        response = self.client.get(HOME_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_drivers"], num_drivers)
        self.assertEqual(
            response.context["num_manufacturers"], num_manufacturers
        )
        self.assertEqual(response.context["num_cars"], num_cars)
        self.assertTemplateUsed(response, "taxi/index.html")
