from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PrivateDriverTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        usernames = (
            "a_driver",
            "drivera",
            "drivar",
            "driver"
        )
        digits = 12345
        for username in usernames:
            get_user_model().objects.create_user(
                username=username,
                password="test12345",
                license_number=f"ABC{digits}"
            )
            digits += 1

    def setUp(self) -> None:
        self.user = get_user_model().objects.get(id=1)
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )

    def test_correct_search_results(self):
        driver_not_in_results = get_user_model().objects.get(username="driver")
        form_data = {
            "username": "A"
        }
        response = self.client.get(reverse("taxi:driver-list"), data=form_data)

        self.assertEqual(len(response.context_data["driver_list"]), 3)
        self.assertTrue(
            driver_not_in_results not in response.context_data["driver_list"]
        )

    def test_assign_to_car(self):
        self.client.get(reverse(
            "taxi:toggle-car-assign",
            kwargs={"pk": self.car.id})
        )
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": self.car.id})
        )

        self.assertContains(response, "Delete me from this car")

    def test_delete_from_car(self):
        self.user.cars.add(self.car)
        self.client.get(
            reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.id})
        )
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": self.car.id})
        )

        self.assertContains(response, "Assign me to this car")

    def test_incorrect_driver_license_update(self):
        license_errors = (
            ("abc12345", "First 3 characters should be uppercase letters"),
            ("ABCD2345", "Last 5 characters should be digits"),
            ("ABC1234", "License number should consist of 8 characters")
        )
        url = reverse("taxi:driver-update", args=[self.user.id])
        for license_number, error in license_errors:
            response = self.client.post(
                url,
                data={"license_number": license_number}
            )

            self.assertContains(response, error)


class PrivateCarTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        manufacturers = (
            ("Toyota", "Japan"),
            ("BMW", "Germany"),
            ("Suzuki", "Japan")
        )
        models = (
            "Corolla",
            "X5",
            "Vitara"
        )
        for index, (name, country) in enumerate(manufacturers):
            manufacturer = Manufacturer.objects.create(
                name=name,
                country=country
            )
            Car.objects.create(
                model=models[index],
                manufacturer=manufacturer
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="test12345",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

    def test_correct_search_results(self):
        model_in_results = Car.objects.get(model="X5")
        form_data = {
            "model": "x"
        }
        response = self.client.get(reverse("taxi:car-list"), data=form_data)

        self.assertEqual(len(response.context_data["car_list"]), 1)
        self.assertTrue(model_in_results in response.context_data["car_list"])


class PrivateManufacturerTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        manufacturers = (
            ("Toyota", "Japan"),
            ("BMW", "Germany"),
            ("Suzuki", "Japan")
        )
        for name, country in manufacturers:
            Manufacturer.objects.create(
                name=name,
                country=country
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="test12345",
            license_number="ABC12345"
        )
        self.client.force_login(self.user)

    def test_correct_search_results(self):
        name_in_results = Manufacturer.objects.get(name="BMW")
        form_data = {
            "name": "w"
        }
        response = self.client.get(
            reverse("taxi:manufacturer-list"), data=form_data
        )

        self.assertEqual(len(response.context_data["manufacturer_list"]), 1)
        self.assertTrue(
            name_in_results in response.context_data["manufacturer_list"]
        )
