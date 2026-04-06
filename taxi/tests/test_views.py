from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicAccessViewTests(TestCase):
    def test_login_required_list(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_login_required_detail(self):
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": 1})
        )
        self.assertNotEqual(response.status_code, 200)


class PrivateAccessViewTests(TestCase):
    def setUp(self):
        driver = get_user_model().objects.create(
            username="test_user",
            password="test12345"
        )
        self.client.force_login(driver)

    def test_login_required_list(self):
        Manufacturer.objects.create(
            name="test_manufacturer1",
            country="test_country1",
        )
        Manufacturer.objects.create(
            name="test_manufacturer2",
            country="test_country2",
        )
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class SearchViewTests(TestCase):
    def setUp(self):
        driver = get_user_model().objects.create(
            username="test_user",
            password="test12345"
        )
        self.client.force_login(driver)

    def test_search_manufacturer(self):
        manufacturer1 = Manufacturer.objects.create(
            name="test_manufacturer1",
            country="test_country1",
        )
        manufacturer2 = Manufacturer.objects.create(
            name="test_manufacturer2",
            country="test_country2",
        )
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"search": "test_manufacturer1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(manufacturer1, response.context["manufacturer_list"])
        self.assertNotIn(manufacturer2, response.context["manufacturer_list"])

    def test_search_driver(self):
        driver1 = get_user_model().objects.create(
            username="test_driver1",
            license_number="ABC12345",
        )
        driver2 = get_user_model().objects.create(
            username="test_driver2",
            license_number="XYZ12345",
        )
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"search": "test_driver1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(driver1, response.context["driver_list"])
        self.assertNotIn(driver2, response.context["driver_list"])

    def test_search_car(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        car1 = Car.objects.create(
            model="X5",
            manufacturer=manufacturer,
        )
        car2 = Car.objects.create(
            model="Audi A6",
            manufacturer=manufacturer,
        )

        response = self.client.get(
            reverse("taxi:car-list"),
            {"search": "X5"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(car1, response.context["car_list"])
        self.assertNotIn(car2, response.context["car_list"])


class AssignToCarTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.driver = get_user_model().objects.create(
            username="test_user",
            password="test12345",
            license_number="ABC12345",
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer1",
            country="test_country1",
        )
        cls.car = Car.objects.create(
            model="X5",
            manufacturer=cls.manufacturer,
        )

    def setUp(self):
        self.client.force_login(self.driver)

    def test_assign_car_driver_add(self):
        self.client.get(
            reverse(
                "taxi:toggle-car-assign",
                args=[self.car.id]
            ),
        )
        self.driver.refresh_from_db()
        self.assertIn(self.car, self.driver.cars.all())

    def test_assign_car_driver_remove(self):
        self.driver.cars.add(self.car)
        self.client.get(
            reverse(
                "taxi:toggle-car-assign",
                args=[self.car.id]
            ),
        )
        self.driver.refresh_from_db()
        self.assertNotIn(self.car, self.driver.cars.all())
