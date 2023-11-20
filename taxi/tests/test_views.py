from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")

NUMBER_OF_MANUFACTURERS = 5
NUMBER_OF_CARS = 5
NUMBER_OF_DRIVERS = 5


class PublicManufacturerListTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PublicCarListTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PublicDriverListTest(TestCase):
    def test_login_required(self) -> None:
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerListTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        manufacturers_to_create = NUMBER_OF_MANUFACTURERS

        for manufacturer_id in range(manufacturers_to_create):
            Manufacturer.objects.create(
                name=f"Manufacturer {manufacturer_id}",
                country=f"Country {manufacturer_id}"
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="username",
            password="password"
        )
        self.client.force_login(self.user)

    def test_get_all_manufacturers(self) -> None:
        response = self.client.get(MANUFACTURER_LIST_URL)

        all_manufacturers = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["manufacturer_list"]),
            NUMBER_OF_MANUFACTURERS
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(all_manufacturers)
        )

    def test_search_manufacturers_by_name(self) -> None:
        search_request1 = "Manufacturer 0"
        search_request2 = "Manufacturer"
        search_request3 = "_"

        # Should have only one manufacturer in it
        response1 = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": search_request1}
        )

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(
            len(response1.context["manufacturer_list"]),
            1
        )
        self.assertEqual(
            list(response1.context["manufacturer_list"]),
            [Manufacturer.objects.all().first()]
        )

        # Should have all manufacturers in it
        response2 = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": search_request2}
        )

        self.assertEqual(response2.status_code, 200)
        self.assertEqual(
            len(response2.context["manufacturer_list"]),
            NUMBER_OF_MANUFACTURERS
        )
        self.assertEqual(
            list(response2.context["manufacturer_list"]),
            list(Manufacturer.objects.all())
        )

        # Should have no manufacturers in it :)
        response3 = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": search_request3}
        )

        self.assertEqual(response3.status_code, 200)
        self.assertEqual(
            len(response3.context["manufacturer_list"]),
            0
        )
        self.assertEqual(
            list(response3.context["manufacturer_list"]),
            list()
        )


class PrivateCarListTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cars_to_create = NUMBER_OF_CARS

        manufacturer = Manufacturer.objects.create(name="Manufacturer")

        for car_id in range(cars_to_create):
            Car.objects.create(
                model=f"Model {car_id}",
                manufacturer=manufacturer
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="username",
            password="password"
        )
        self.client.force_login(self.user)

    def test_get_all_cars(self) -> None:
        response = self.client.get(CAR_LIST_URL)

        all_cars = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["car_list"]),
            NUMBER_OF_CARS
        )
        self.assertEqual(
            list(response.context["car_list"]),
            list(all_cars)
        )

    def test_search_cars_by_model(self) -> None:
        search_request1 = "Model 0"
        search_request2 = "Model"
        search_request3 = "_"

        # Should have only one car in it
        response1 = self.client.get(
            reverse("taxi:car-list"),
            {"model": search_request1}
        )

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(
            len(response1.context["car_list"]),
            1
        )
        self.assertEqual(
            list(response1.context["car_list"]),
            [Car.objects.all().first()]
        )

        # Should have all cars in it
        response2 = self.client.get(
            reverse("taxi:car-list"),
            {"model": search_request2}
        )

        self.assertEqual(response2.status_code, 200)
        self.assertEqual(
            len(response2.context["car_list"]),
            NUMBER_OF_CARS
        )
        self.assertEqual(
            list(response2.context["car_list"]),
            list(Car.objects.all())
        )

        # Should have no cars in it
        response3 = self.client.get(
            reverse("taxi:car-list"),
            {"model": search_request3}
        )

        self.assertEqual(response3.status_code, 200)
        self.assertEqual(
            len(response3.context["car_list"]),
            0
        )
        self.assertEqual(
            list(response3.context["car_list"]),
            list()
        )


class PrivateDriverListTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        drivers_to_create = NUMBER_OF_DRIVERS

        for driver_id in range(drivers_to_create):
            get_user_model().objects.create_user(
                username=f"driver{driver_id}",
                password=f"drvr{driver_id}",
                first_name=f"first_name {driver_id}",
                last_name=f"last_name {driver_id}",
                license_number=f"ABC{driver_id * 11111}"
            )

    def setUp(self) -> None:
        self.client.force_login(get_user_model().objects.all().first())

    def test_get_all_drivers(self) -> None:
        response = self.client.get(DRIVER_LIST_URL)

        all_drivers = Driver.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["driver_list"]),
            NUMBER_OF_DRIVERS
        )
        self.assertEqual(
            list(response.context["driver_list"]),
            list(all_drivers)
        )

    def test_search_drivers_by_username(self) -> None:
        search_request1 = "driver0"
        search_request2 = "driver"
        search_request3 = "_"

        # Should have only one driver in it
        response1 = self.client.get(
            reverse("taxi:driver-list"),
            {"username": search_request1}
        )

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(
            len(response1.context["driver_list"]),
            1
        )
        self.assertEqual(
            list(response1.context["driver_list"]),
            [Driver.objects.all().first()]
        )

        # Should have all drivers in it
        response2 = self.client.get(
            reverse("taxi:driver-list"),
            {"username": search_request2}
        )

        self.assertEqual(response2.status_code, 200)
        self.assertEqual(
            len(response2.context["driver_list"]),
            NUMBER_OF_DRIVERS
        )
        self.assertEqual(
            list(response2.context["driver_list"]),
            list(Driver.objects.all())
        )

        # Should have no cars in it
        response3 = self.client.get(
            reverse("taxi:driver-list"),
            {"username": search_request3}
        )

        self.assertEqual(response3.status_code, 200)
        self.assertEqual(
            len(response3.context["driver_list"]),
            0
        )
        self.assertEqual(
            list(response3.context["driver_list"]),
            list()
        )
