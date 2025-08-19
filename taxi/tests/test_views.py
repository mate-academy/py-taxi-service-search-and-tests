from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.forms import ManufacturerSearchForm
from taxi.models import Manufacturer, Car


class ManufacturerListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="user",
            password="pass1234"
        )

        number_of_manufacturers = 12

        for manufacturer_id in range(number_of_manufacturers):
            Manufacturer.objects.create(
                name=f"Name {manufacturer_id}",
                country=f"Countre {manufacturer_id}"
            )

    def setUp(self):
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/manufacturers/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class ManufacturerSearchFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="user",
            password="pass1234"
        )
        cls.drivers = [
            get_user_model().objects.create_user(
                username="user1",
                email="user1@user.com",
                license_number="ABC12349",
                password="pass1235"
            ),
            get_user_model().objects.create_user(
                username="user2",
                email="user2@user.com",
                license_number="ABC14349",
                password="PASS1234"
            ),
            get_user_model().objects.create_user(
                username="Mykola",
                email="mykola@user.com",
                license_number="ABC92349",
                password="passPASS"
            ),
        ]
        cls.manufacturers = [
            Manufacturer.objects.create(name="Ford", country="USA"),
            Manufacturer.objects.create(name="Toyota", country="Japan"),
            Manufacturer.objects.create(name="Fiat", country="Italy")
        ]
        cls.cars = [
            Car.objects.create(
                model="Focus",
                manufacturer=cls.manufacturers[0]
            ),
            Car.objects.create(
                model="Pocus",
                manufacturer=cls.manufacturers[0]
            ),
            Car.objects.create(
                model="Kuga",
                manufacturer=cls.manufacturers[0]
            ),
            Car.objects.create(
                model="Corolla",
                manufacturer=cls.manufacturers[1]
            ),
            Car.objects.create(
                model="500",
                manufacturer=cls.manufacturers[2]
            ),
        ]

    def setUp(self):
        self.client.force_login(self.user)

    def test_search_manufacturers(self):
        response = self.client.get("/manufacturers/?name=o")
        manufacturer_list = response.context["manufacturer_list"]
        self.assertEqual(len(manufacturer_list), 2)
        self.assertEqual(manufacturer_list[0].name, "Ford")

    def test_search_cars(self):
        response = self.client.get("/cars/?model=us")
        car_list = response.context["car_list"]
        self.assertEqual(len(car_list), 2)

    def test_search_drivers(self):
        response = self.client.get("/drivers/?username=user")
        driver_list = response.context["driver_list"]
        self.assertEqual(len(driver_list), 2)
