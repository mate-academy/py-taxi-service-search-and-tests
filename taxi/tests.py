from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Manufacturer, Driver, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="US",
        )
        self.assertEqual(str(manufacturer), "Test Manufacturer"" ""US")

    def test_driver_str(self):
        driver = Driver.objects.create(
            username="Test Driver",
            first_name="Test first name",
            last_name="Test last name",
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="TestCar",
            country="TestCountry",
        )
        car = Car.objects.create(
            model="testmodelcar",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), "testmodelcar")


class PublicIndexViewTest(TestCase):
    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/")


class PrivateIndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass",
            license_number="AAA12345"
        )
        self.client.force_login(self.user)

    def test_index_view_status_code_and_template(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")

    def test_index_view_context_data(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Car.objects.create(
            model="X5",
            manufacturer=Manufacturer.objects.first()
        )
        response = self.client.get(reverse("taxi:index"))
        self.assertIn("num_drivers", response.context)
        self.assertIn("num_cars", response.context)
        self.assertIn("num_manufacturers", response.context)
        self.assertIn("num_visits", response.context)
        self.assertEqual(response.context["num_drivers"], 1)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_manufacturers"], 1)


class SearchViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass",
            license_number="AAA12345"
        )
        self.client.force_login(self.user)

    def test_manufacturer_search(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Toyota", country="Japan")
        url = reverse("taxi:manufacturer-list") + "?title="
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BMW")
        self.assertContains(response, "Toyota")

    def test_car_search(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        Car.objects.create(model="X5", manufacturer=manufacturer)
        Car.objects.create(model="Corolla", manufacturer=manufacturer)

        url = reverse("taxi:car-list") + "?title="
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_driver_search(self):
        Driver.objects.create_user(
            username="driver1",
            password="pass",
            license_number="AAA00001",
            first_name="John",
            last_name="Doe"
        )
        Driver.objects.create_user(
            username="driver2",
            password="pass",
            license_number="BBB00002",
            first_name="Jane",
            last_name="Smith"
        )
        url = reverse("taxi:driver-list") + "?title="
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver1")
        self.assertContains(response, "driver2")
