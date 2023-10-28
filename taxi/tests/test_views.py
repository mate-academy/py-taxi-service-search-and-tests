from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer

HOME_URL = reverse("taxi:index")
MANUFACTURERS_URL = reverse("taxi:manufacturer-list")
DRIVERS_URL = reverse("taxi:driver-list")
CARS_URL = reverse("taxi:car-list")


class TestViewsLoginRequired(TestCase):
    def test_login_required_home(self):
        response = self.client.get(HOME_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_cars_list(self):
        response = self.client.get(CARS_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_drivers_list(self):
        response = self.client.get(DRIVERS_URL)
        self.assertNotEquals(response.status_code, 200)

    def test_login_required_manufacturers_list(self):
        response = self.client.get(MANUFACTURERS_URL)
        self.assertNotEquals(response.status_code, 200)


class TestViewsPagesForRegisteredUser(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="rambo1982",
            password="JustWantToEatButHaveToKill82",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Volvo", country="Sweden")

        response = self.client.get(MANUFACTURERS_URL)
        self.assertEquals(response.status_code, 200)

        manufacturers = Manufacturer.objects.all()
        self.assertEquals(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class ToggleAssignToCarTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        self.car1 = Car.objects.create(
            model="M3",
            manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="M5",
            manufacturer=self.manufacturer
        )
        self.driver = Driver.objects.create(
            username="testuser",
            license_number="BMW35678"
        )
        self.client.login(
            username="testuser",
            password="password"
        )
        self.client.force_login(self.driver)

    def test_remove_assign_car(self):
        url = reverse(
            "taxi:toggle-car-assign",
            kwargs={"pk": self.car1.pk}
        )
        self.driver.cars.add(self.car1)
        initial_driver_cars_count = self.driver.cars.count()
        response = self.client.post(url)
        self.driver.refresh_from_db()
        updated_driver_cars_count = self.driver.cars.count()
        self.assertEqual(
            updated_driver_cars_count,
            initial_driver_cars_count - 1
        )
        self.assertRedirects(
            response,
            reverse(
                "taxi:car-detail",
                args=[self.car1.pk]
            )
        )

    def test_add_assign_car(self):
        url = reverse(
            "taxi:toggle-car-assign",
            kwargs={"pk": self.car2.pk}
        )
        self.driver.cars.add(self.car1)
        initial_driver_cars_count = self.driver.cars.count()
        response = self.client.post(url)

        self.driver.refresh_from_db()
        updated_driver_cars_count = self.driver.cars.count()

        self.assertEqual(
            updated_driver_cars_count,
            initial_driver_cars_count + 1
        )
        self.assertRedirects(
            response,
            reverse(
                "taxi:car-detail",
                args=[self.car2.pk]
            )
        )
