from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class AuthenticatedViewTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345",
        )

    def test_index_requires_login(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('taxi:index')}",
        )

    def test_index_shows_counts_and_increments_visits(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        Car.objects.create(model="Camry", manufacturer=manufacturer)
        Driver.objects.create_user(
            username="second",
            password="testpass123",
            license_number="XYZ67890",
        )

        self.client.login(username="testuser", password="testpass123")

        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_manufacturers"], 1)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_drivers"], 2)
        self.assertEqual(response.context["num_visits"], 1)

        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.context["num_visits"], 2)


class ManufacturerSearchTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345",
        )
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="Volkswagen", country="Germany")

    def setUp(self):
        self.client.login(username="testuser", password="testpass123")

    def test_search_filters_manufacturers_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "toy"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            [Manufacturer.objects.get(name="Toyota")],
        )

    def test_search_is_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "FORD"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            [Manufacturer.objects.get(name="Ford")],
        )

    def test_search_form_keeps_entered_value(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "toy"},
        )

        self.assertEqual(
            response.context["search_form"].initial["name"],
            "toy",
        )


class CarSearchTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345",
        )
        cls.toyota = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        cls.ford = Manufacturer.objects.create(
            name="Ford",
            country="USA",
        )
        Car.objects.create(model="Camry", manufacturer=cls.toyota)
        Car.objects.create(model="Corolla", manufacturer=cls.toyota)
        Car.objects.create(model="Focus", manufacturer=cls.ford)

    def setUp(self):
        self.client.login(username="testuser", password="testpass123")

    def test_search_filters_cars_by_model(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "cam"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            [Car.objects.get(model="Camry")],
        )

    def test_search_is_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "FOC"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            [Car.objects.get(model="Focus")],
        )


class DriverSearchTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345",
        )
        Driver.objects.create_user(
            username="alex",
            password="testpass123",
            license_number="XYZ12345",
        )
        Driver.objects.create_user(
            username="alexander",
            password="testpass123",
            license_number="XYZ67890",
        )
        Driver.objects.create_user(
            username="john",
            password="testpass123",
            license_number="DEF12345",
        )

    def setUp(self):
        self.client.login(username="testuser", password="testpass123")

    def test_search_filters_drivers_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "alex"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            set(response.context["driver_list"]),
            {
                Driver.objects.get(username="alex"),
                Driver.objects.get(username="alexander"),
            },
        )

    def test_search_is_case_insensitive(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "JOHN"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            [Driver.objects.get(username="john")],
        )


class ToggleAssignToCarTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="testuser",
            password="testpass123",
            license_number="ABC12345",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer,
        )
        self.client.login(username="testuser", password="testpass123")

    def test_toggle_assign_adds_driver_to_car(self):
        response = self.client.get(
            reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.pk})
        )

        self.assertRedirects(
            response,
            reverse("taxi:car-detail", kwargs={"pk": self.car.pk}),
        )
        self.assertIn(self.car, self.driver.cars.all())

    def test_toggle_assign_removes_driver_from_car(self):
        self.driver.cars.add(self.car)

        response = self.client.get(
            reverse("taxi:toggle-car-assign", kwargs={"pk": self.car.pk})
        )

        self.assertRedirects(
            response,
            reverse("taxi:car-detail", kwargs={"pk": self.car.pk}),
        )
        self.assertNotIn(self.car, self.driver.cars.all())
