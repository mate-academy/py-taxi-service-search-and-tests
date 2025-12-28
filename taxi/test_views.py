from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver
from taxi.forms import DriverUsernameSearchForm

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")

User = get_user_model()


class PublicManufacturerTests(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="BMW")
        Manufacturer.objects.create(name="Porsche")

        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)

        manufacturers = Manufacturer.objects.all()

        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PublicCarTests(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin",
            password="admin",
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        manufacturer = Manufacturer.objects.create(name="BMW")
        Car.objects.create(model="i4 Competition", manufacturer=manufacturer)
        Car.objects.create(model="M5 F90", manufacturer=manufacturer)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PublicDriverTests(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"/accounts/login/?next={DRIVER_URL}")


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testadmin", password="testpassword"
        )
        self.client.force_login(self.user)
        Driver.objects.create(username="driver1", license_number="LIC0001")
        Driver.objects.create(username="driver2", license_number="LIC0002")

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        expected_queryset = Driver.objects.filter(
            username__icontains=self.user.username
        )
        self.assertEqual(
            list(response.context["driver_list"]),
            list(expected_queryset)
        )
        self.assertTemplateUsed(
            response, "taxi/driver_list.html"
        )

    def test_search_drivers_by_username(self):
        response = self.client.get(DRIVER_URL + "?username=driver1")
        self.assertEqual(response.status_code, 200)
        filtered_drivers = Driver.objects.filter(
            username__icontains="driver1"
        )
        self.assertEqual(
            list(response.context["driver_list"]),
            list(filtered_drivers)
        )
        self.assertIn("search_form", response.context)
        self.assertIsInstance(response.context["search_form"],
                              DriverUsernameSearchForm
                              )
        self.assertTemplateUsed(
            response, "taxi/driver_list.html"
        )


class ToggleAssignToCarTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="12345", license_number="ABC123"
        )
        self.driver = Driver.objects.get(username="testuser")
        self.car1 = Car.objects.create(
            model="Model X",
            manufacturer=Manufacturer.objects.create(
                name="Tesla",
                country="USA"
            ),
        )
        self.car2 = Car.objects.create(
            model="i4 Competition",
            manufacturer=Manufacturer.objects.create(
                name="BMW",
                country="Germany"
            ),
        )
        self.url = reverse(
            "taxi:toggle-car-assign",
            kwargs={"pk": self.car1.pk}
        )
        self.client.login(username="testuser", password="12345")

    def test_add_car_to_driver(self):
        response = self.client.post(self.url)
        self.driver.refresh_from_db()
        self.assertIn(self.car1, self.driver.cars.all())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            "taxi:car-detail", args=[self.car1.pk]
        ))

    def test_remove_car_from_driver(self):
        self.driver.cars.add(self.car1)
        response = self.client.post(self.url)
        self.driver.refresh_from_db()
        self.assertNotIn(self.car1, self.driver.cars.all())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            "taxi:car-detail", args=[self.car1.pk]
        ))
