from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            f"/accounts/login/?next={CAR_LIST_URL}"
        )


class PrivateCarTest(TestCase):
    def setUp(self):
        for i in range(10):
            manufacturer = Manufacturer.objects.create(
                name=f"manufacturer_name_{i}",
                country=f"manufacturer_country_{i}"
            )
            Car.objects.create(
                model=f"test_{i}",
                manufacturer=manufacturer
            )

        user = get_user_model().objects.create(
            username="Username_test",
            password="Password123!",
            license_number="PZT12345"
        )
        self.client.force_login(user)

    def test_all_cars(self):
        paginated_by = 5
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.all())[:paginated_by]
        )

    def test_search_car_by_model(self):
        searched_model = "test_9"
        response = self.client.get(CAR_LIST_URL, {"model": searched_model})

        self.assertEqual(
            response.context["car_list"][0],
            Car.objects.get(model=searched_model)
        )


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            f"/accounts/login/?next={DRIVER_LIST_URL}"
        )


class PrivateDriverTest(TestCase):
    def setUp(self):
        for i in range(10):
            get_user_model().objects.create(
                username=f"test_{i}",
                password=f"test_password{i}!",
                license_number=f"VVV123{i}5"
            )

        user = get_user_model().objects.create(
            username="Username_test",
            password="Password123!",
            license_number="PZT12345"
        )
        self.client.force_login(user)

    def test_all_drivers(self):
        paginated_by = 5
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(get_user_model().objects.all())[:paginated_by]
        )

    def test_search_driver_by_username(self):
        searched_username = "test_9"
        response = self.client.get(
            DRIVER_LIST_URL,
            {"username": searched_username}
        )

        self.assertEqual(
            response.context["driver_list"][0],
            get_user_model().objects.get(username=searched_username)
        )


class PublicManufacturerTest(TestCase):
    def test_login_required(self):

        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            f"/accounts/login/?next={MANUFACTURER_LIST_URL}"
        )


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        for i in range(10):
            Manufacturer.objects.create(
                name=f"test_{i}",
                country=f"test_country_{i}"
            )

        user = get_user_model().objects.create(
            username="Username_test",
            password="Password123!",
            license_number="PVT12345"
        )
        self.client.force_login(user)

    def test_all_manufacturer(self):
        paginated_by = 5
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.all())[:paginated_by]
        )

    def test_search_manufacturer_by_name(self):
        searched_name = "test_9"
        response = self.client.get(
            MANUFACTURER_LIST_URL,
            {"name": searched_name}
        )

        self.assertEqual(
            response.context["manufacturer_list"][0],
            Manufacturer.objects.get(name=searched_name)
        )
