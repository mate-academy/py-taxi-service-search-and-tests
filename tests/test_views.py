from django.conf.global_settings import LOGIN_URL
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"{LOGIN_URL}?next={MANUFACTURER_URL}")


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        for i in range(25):
            Manufacturer.objects.create(
                name=f"test{i}",
                country=f"test_country{i}"
            )
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="password12345"
        )
        self.client.force_login(self.driver)

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        manufacturers = Manufacturer.objects.all()
        paginator = Paginator(manufacturers, 5)
        num_of_pages = paginator.num_pages

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

        for num_of_page in range(1, num_of_pages + 1):
            response = self.client.get(MANUFACTURER_URL, {"page": num_of_page})

            self.assertEqual(
                list(response.context["manufacturer_list"]),
                list(paginator.get_page(num_of_page))
            )

    def test_search_manufacturer_by_part_name(self):
        searched_part_name = "2"
        manufacturers = Manufacturer.objects.filter(
            name__icontains=searched_part_name
        )
        paginator = Paginator(manufacturers, 5)
        num_of_pages = paginator.num_pages

        for num_of_page in range(1, num_of_pages + 1):
            response = self.client.get(
                MANUFACTURER_URL,
                {"name": searched_part_name, "page": num_of_page}
            )

            self.assertEqual(
                list(response.context["manufacturer_list"]),
                list(paginator.get_page(num_of_page))
            )


class PublicDriverTests(TestCase):
    def setUp(self) -> None:
        for i in range(24):
            get_user_model().objects.create(
                username=f"test{i}",
                password=f"password{i}",
                license_number=f"license{i}"
            )

    def test_login_required(self):
        response = self.client.get(DRIVER_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"{LOGIN_URL}?next={DRIVER_URL}")

        for driver in get_user_model().objects.all():
            expected_url = reverse("taxi:driver-detail", args=[driver.id])
            detail_response = self.client.get(expected_url)

            self.assertNotEqual(
                f"{detail_response.status_code}/{driver.id}",
                200
            )


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        for i in range(24):
            get_user_model().objects.create(
                username=f"test{i}",
                password=f"password{i}",
                license_number=f"license{i}"
            )
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="password12345",
            license_number="TST12345"
        )
        self.client.force_login(self.driver)

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_URL)
        drivers = get_user_model().objects.all()
        paginator = Paginator(drivers, 5)
        num_of_pages = paginator.num_pages

        self.assertEqual(response.status_code, 200)

        for num_of_page in range(1, num_of_pages + 1):
            response = self.client.get(DRIVER_URL, {"page": num_of_page})

            self.assertEqual(
                list(response.context["driver_list"]),
                list(paginator.get_page(num_of_page))
            )

    def test_search_driver_by_part_username(self):
        searched_part_username = "2"
        drivers = get_user_model().objects.filter(
            username__icontains=searched_part_username
        )
        paginator = Paginator(drivers, 5)
        num_of_pages = paginator.num_pages

        for num_of_page in range(1, num_of_pages + 1):
            response = self.client.get(
                DRIVER_URL,
                {
                    "username": searched_part_username,
                    "page": num_of_page
                }
            )

            self.assertEqual(
                list(response.context["driver_list"]),
                list(paginator.get_page(num_of_page))
            )


class PublicCarTests(TestCase):
    def setUp(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        for i in range(24):
            Car.objects.create(
                model=f"test{i}",
                manufacturer=manufacturer,
            )

    def test_login_required(self):
        response = self.client.get(CAR_URL)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"{LOGIN_URL}?next={CAR_URL}")

        for car in Car.objects.all():
            expected_url = reverse("taxi:car-detail", args=[car.id])
            detail_response = self.client.get(expected_url)

            self.assertNotEqual(f"{detail_response.status_code}/{car.id}", 200)


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="test_name",
            country="test_country"
        )
        for i in range(24):
            Car.objects.create(
                model=f"test{i}",
                manufacturer=manufacturer,
            )
        self.driver = get_user_model().objects.create_user(
            username="test",
            password="password12345",
            license_number="TST12345"
        )
        self.client.force_login(self.driver)

    def test_retrieve_cars(self):
        response = self.client.get(CAR_URL)
        cars = Car.objects.all()
        paginator = Paginator(cars, 5)
        num_of_pages = paginator.num_pages

        self.assertEqual(response.status_code, 200)

        for num_of_page in range(1, num_of_pages + 1):
            response = self.client.get(CAR_URL, {"page": num_of_page})

            self.assertEqual(
                list(response.context["car_list"]),
                list(paginator.get_page(num_of_page))
            )

    def test_search_car_by_part_model(self):
        searched_part_model = "2"
        cars = Car.objects.filter(model__icontains=searched_part_model)
        paginator = Paginator(cars, 5)
        num_of_pages = paginator.num_pages

        for num_of_page in range(1, num_of_pages + 1):
            response = self.client.get(
                CAR_URL,
                {
                    "model": searched_part_model,
                    "page": num_of_page
                }
            )

            self.assertEqual(
                list(response.context["car_list"]),
                list(paginator.get_page(num_of_page))
            )
