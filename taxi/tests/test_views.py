from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")
USERNAME = "user12"
PASSWORD = "user12345"
MANUFACTURERS = [
    ("KIA", "China"),
    ("AUDI", "Germany"),
    ("FORD", "USA"),
    ("FIAT", "Italy")
]
CARS = ["Stinger", "A7", "Mustang", "Punto"]
DRIVERS = [
    {
        "username": "driver_1",
        "first_name": "first_1",
        "last_name": "last_1",
        "license_number": "ABC12345"
    },
    {
        "username": "driver_2",
        "first_name": "first_2",
        "last_name": "last_2",
        "license_number": "DEF12345"
    },
    {
        "username": "driver_3",
        "first_name": "first_3",
        "last_name": "last_3",
        "license_number": "CBA12345"
    }
]


class PublicViewsTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_manufacturer_login_required(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertNotEquals(response.status_code, 200)

    def test_car_login_required(self):
        response = self.client.get(CAR_URL)

        self.assertNotEquals(response.status_code, 200)

    def test_driver_login_required(self):
        response = self.client.get(DRIVER_URL)

        self.assertNotEquals(response.status_code, 200)


class PrivateManufacturerViewsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username=USERNAME,
            password=PASSWORD
        )

        self.client.force_login(self.user)

    @classmethod
    def setUpTestData(cls):
        for manufacturer in MANUFACTURERS:
            Manufacturer.objects.create(
                name=manufacturer[0],
                country=manufacturer[1]
            )

    def test_retrieve_manufacturer(self):
        response = self.client.get(MANUFACTURER_URL)
        manufacturers_list = Manufacturer.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["manufacturer_list"]),
            list(manufacturers_list)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_search_form(self):
        search_value = "Au"
        url = reverse("taxi:manufacturer-list") + f"?name={search_value}"
        response = self.client.get(url)
        manufacturer_query = Manufacturer.objects.filter(
            name__icontains=search_value
        )
        self.assertEquals(
            list(response.context["manufacturer_list"]),
            list(manufacturer_query)
        )


class PrivateCarViewsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username=USERNAME,
            password=PASSWORD
        )
        self.client.force_login(self.user)

    @classmethod
    def setUpTestData(cls):
        for manufacturer in MANUFACTURERS:
            Manufacturer.objects.create(
                name=manufacturer[0],
                country=manufacturer[1]
            )

        for car in range(len(CARS)):
            Car.objects.create(
                model=CARS[car],
                manufacturer=Manufacturer.objects.get(id=car + 1)
            )

    def test_retrieve_car(self):
        response = self.client.get(CAR_URL)
        car_list = Car.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["car_list"]),
            list(car_list)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_search_form(self):
        search_value = "Sti"
        url = reverse("taxi:car-list") + f"?model={search_value}"
        response = self.client.get(url)
        car_query = Car.objects.filter(
            model__icontains=search_value
        )

        self.assertEquals(
            list(response.context["car_list"]),
            list(car_query)
        )


class PrivateDriverViewsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username=USERNAME,
            password=PASSWORD
        )
        self.client.force_login(self.user)

    @classmethod
    def setUpTestData(cls):
        for driver in DRIVERS:
            get_user_model().objects.create(
                username=driver["username"],
                first_name=driver["first_name"],
                last_name=driver["last_name"],
                license_number=driver["license_number"]
            )

    def test_retrieve_driver(self):
        response = self.client.get(DRIVER_URL)
        driver_list = get_user_model().objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["driver_list"]),
            list(driver_list)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_search_form(self):
        search_value = "_2"
        url = reverse("taxi:driver-list") + f"?username={search_value}"
        response = self.client.get(url)
        driver_query = get_user_model().objects.filter(
            username__icontains=search_value
        )

        self.assertEquals(
            list(response.context["driver_list"]),
            list(driver_query)
        )
