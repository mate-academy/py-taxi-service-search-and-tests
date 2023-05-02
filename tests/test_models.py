from django.contrib.auth import get_user_model
from django.test import TestCase

from taxi.models import Car, Driver, Manufacturer


class ModelsTests(TestCase):
    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Opel",
            country="Germany",
        )
        car = Car.objects.create(model="Astra", manufacturer=manufacturer)
        self.assertEqual(str(car), "Astra")

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="JohnDoe",
            password="somepassword123",
            first_name="John",
            last_name="Doe",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Opel",
            country="Germany",
        )
        self.assertEqual(
            str(manufacturer), f"{manufacturer.name} {manufacturer.country}"
        )

    def create_driver_with_license(self):
        driver = get_user_model().objects.create_user(
            username="JaneDoe",
            password="somepassword456",
            first_name="Jane",
            last_name="Doe",
            license_number="ASD45678",
        )
        self.assertEqual(driver.username, "JaneDoe")
        self.assertEqual(driver.license_number, "ASD45678")
        self.assertTrue(driver.check_password("somepassword456"))


class SearchFormsTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="somepassword123",
        )
        self.client.force_login(self.user)

    def test_manufacturer_search(self):
        search_term = "test_manufacturer"
        response = self.client.get(
            f"/manufacturers/?username={search_term}"
        )

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            Manufacturer.objects.filter(name__icontains=search_term)
        )

    def test_car_search(self):
        search_term = "test_car"
        response = self.client.get(f"/cars/?username={search_term}")

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["car_list"],
            Car.objects.filter(model__icontains=search_term)
        )

    def test_driver_search(self):
        search_term = "test_driver"
        response = self.client.get(f"/drivers/?username={search_term}")

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["driver_list"],
            get_user_model().objects.filter(username__icontains=search_term)
        )
