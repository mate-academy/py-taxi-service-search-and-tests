from django.test import TestCase
from django.urls import reverse
from taxi.models import Car, Driver, Manufacturer
from django.contrib.auth import get_user_model


class ListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Користувач для логіну
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="pass"
        )

        # Manufacturer та Car
        cls.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        for i in range(7):
            Car.objects.create(
                model=f"Model{i}",
                manufacturer=cls.manufacturer
            )

        # Drivers
        for i in range(7):
            Driver.objects.create_user(
                username=f"driver{i}",
                password="pass",
                license_number=f"LIC{str(i + 1).zfill(5)}"
            )

        # Додаткові для пошуку
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Car.objects.create(model="SpecialCar", manufacturer=cls.manufacturer)
        Driver.objects.create_user(
            username="specialdriver",
            password="pass",
            license_number="LIC00008"
        )

    def setUp(self):
        self.client.login(username="testuser", password="pass")

    # --- ManufacturerListView ---
    def test_manufacturer_list_view_status(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_search(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-list"
        ) + "?name=Toyota")
        self.assertContains(response, "Toyota")
        self.assertEqual(len(response.context["manufacturer_list"]), 1)

    # --- CarListView ---
    def test_car_list_view_status(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

    def test_car_search(self):
        response = self.client.get(reverse(
            "taxi:car-list"
        ) + "?model=SpecialCar")
        self.assertContains(response, "SpecialCar")
        self.assertEqual(len(response.context["car_list"]), 1)

    # --- DriverListView ---
    def test_driver_list_view_status(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)

    def test_driver_search(self):
        response = self.client.get(reverse(
            "taxi:driver-list"
        ) + "?username=specialdriver")
        self.assertContains(response, "specialdriver")
        self.assertEqual(len(response.context["driver_list"]), 1)
