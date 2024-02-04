from django.contrib.auth import get_user_model
from django.urls import reverse

from django.test import TestCase

from taxi.models import Manufacturer, Car
from taxi.views import ManufacturerListView, CarListView, DriverListView


class TestIndex(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="user-user", password="qwerty123456", license_number="124"
        )

        self.url = reverse("taxi:index")

    def test_login_required(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

        self.client.force_login(self.driver)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_index_context_num_drivers(self):
        self.client.force_login(self.driver)
        response = self.client.get(self.url)
        self.assertEqual(response.context["num_drivers"], 1)

    def test_index_context_num_manufacturers(self):
        for _ in range(10):
            Manufacturer.objects.create(
                name=f"Car manufacturer{_}",
                country="USA")
        self.client.force_login(self.driver)
        response = self.client.get(self.url)
        self.assertEqual(response.context["num_manufacturers"], 10)

    def test_index_context_num_cars(self):
        for _ in range(22):
            Manufacturer.objects.create(
                name=f"Car manufacturer{_}",
                country="USA")
            Car.objects.create(
                model=f"Car model{_}",
                manufacturer=Manufacturer.objects.get(id=_ + 1)
            )
        self.client.force_login(self.driver)
        response = self.client.get(self.url)
        self.assertEqual(response.context["num_cars"], 22)

    def test_index_context_num_visits(self):
        self.client.force_login(self.driver)
        for _ in range(122):
            response = self.client.get(self.url)
        self.assertEqual(response.context["num_visits"], 122)


class TestManufacturerList(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="user-user", password="qwerty123456", license_number="124"
        )

    def test_search_with_pagination(self):
        for _ in range(6):
            Manufacturer.objects.create(name=f"BMW{_}", country="USA")
        for _ in range(110):
            Manufacturer.objects.create(
                name=f"Car manufacturer{_}",
                country="USA")
        ManufacturerListView.paginate_by = 5
        self.client.force_login(self.driver)
        url = (reverse("taxi:manufacturer-list")
               + "?manufacturer_name=BMw&page=2")
        response = self.client.get(url)
        self.assertEqual(len(response.context["object_list"]), 1)


class TestCarList(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="user-user", password="qwerty123456", license_number="124"
        )

    def test_search_with_pagination(self):
        manufacturer = Manufacturer.objects.create(
            name="Car manufacturer", country="USA"
        )
        for _ in range(8):
            Car.objects.create(
                model=f"Peugeot 310{_}",
                manufacturer=manufacturer)
        for _ in range(25):
            Car.objects.create(
                model=f"Car model{_}",
                manufacturer=manufacturer)
        CarListView.paginate_by = 5
        self.client.force_login(self.driver)
        url = reverse("taxi:car-list") + "?car_model=eugeOt&page=2"
        response = self.client.get(url)
        self.assertEqual(len(response.context["object_list"]), 3)


class TestDriverList(TestCase):
    def test_search_with_pagination(self):
        for _ in range(18):
            get_user_model().objects.create_user(
                username=f"userRed{_}",
                password="qwerty123456",
                license_number=f"124{_}",
            )
        for _ in range(28):
            get_user_model().objects.create_user(
                username=f"user{_}",
                password="qwerty123456",
                license_number=f"2324{_}"
            )
        DriverListView.paginate_by = 10
        self.client.force_login(get_user_model().objects.get(id=27))
        url = reverse("taxi:driver-list") + "?driver_username=red&page=2"
        response = self.client.get(url)
        self.assertEqual(len(response.context["object_list"]), 8)
