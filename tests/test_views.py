from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class PublicManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        """
        PublicManufacturerTest:
        Test that accessing the manufacturer list page requires login.
        """
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )

        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        """
        PrivateManufacturerTest:
        Test retrieving the list of manufacturers when logged in.
        """
        Manufacturer.objects.create(name="Subaru", country="Japan")
        Manufacturer.objects.create(name="Renault", country="France")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class ManufacturerSearchTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

        # Create manufacturers for testing
        Manufacturer.objects.create(name="Subaru", country="Japan")
        Manufacturer.objects.create(name="Renault", country="France")
        Manufacturer.objects.create(name="Toyota", country="Japan")

    def test_manufacturer_search(self):
        """
        Test searching for manufacturers by name.
        """
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {'name': 'Sub'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Subaru")
        self.assertNotContains(response, "Renault")
        self.assertNotContains(response, "Toyota")


class PublicCarTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        """
        PublicCarTest:
        Test that accessing the car list page requires login.
        """
        res = self.client.get(CAR_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )

        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        """
        PrivateCarTest:
        Test retrieving the list of cars when logged in.
        """
        manufacturer = Manufacturer.objects.create(
            name="Subaru", country="Japan"
        )
        Car.objects.create(model="Impreza", manufacturer=manufacturer)
        Car.objects.create(model="Legacy", manufacturer=manufacturer)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")


class CarSearchTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

        manufacturer1 = Manufacturer.objects.create(name="Subaru", country="Japan")
        manufacturer2 = Manufacturer.objects.create(name="Renault", country="France")

        Car.objects.create(model="Impreza", manufacturer=manufacturer1)
        Car.objects.create(model="Legacy", manufacturer=manufacturer1)
        Car.objects.create(model="Clio", manufacturer=manufacturer2)

    def test_car_search(self):
        """
        Test searching for cars by model.
        """
        url = reverse("taxi:car-list")

        response = self.client.get(url, {'model': 'Imp'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Impreza")
        self.assertNotContains(response, "Legacy")
        self.assertNotContains(response, "Clio")


class PublicDriverTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required(self):
        """
        PublicDriverTest:
        Test that accessing the driver list page requires login.
        """
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )

        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        """
        PrivateDriverTest:
        Test retrieving the list of drivers when logged in.
        """
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class DriverSearchTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.force_login(self.user)

        Driver.objects.create(username="driver1", password="password1", license_number="CCC12345")
        Driver.objects.create(username="driver2", password="password2", license_number="BBB12345")
        Driver.objects.create(username="user3", password="password3", license_number="AAA12345")

    def test_driver_search(self):
        """
        Test searching for drivers by username.
        """
        url = reverse("taxi:driver-list")

        response = self.client.get(url, {'username': 'driver'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "driver1")
        self.assertContains(response, "driver2")
        self.assertNotContains(response, "user3")


class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )

        self.client.force_login(self.user)

    def test_index_view(self):
        """
        IndexViewTest:
        Test the behavior of the index view.
        """
        subaru = Manufacturer.objects.create(name="Subaru", country="Japan")
        renault = Manufacturer.objects.create(name="Renault", country="France")
        Car.objects.create(model="Car1", manufacturer=subaru)
        Car.objects.create(model="Car2", manufacturer=renault)

        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)

        # Check context variables
        self.assertIn("num_drivers", response.context)
        self.assertIn("num_cars", response.context)
        self.assertIn("num_manufacturers", response.context)
        self.assertIn("num_visits", response.context)

        # Check counts
        self.assertEqual(
            response.context["num_drivers"], Driver.objects.count()
        )
        self.assertEqual(
            response.context["num_cars"], Car.objects.count()
        )
        self.assertEqual(
            response.context["num_manufacturers"], Manufacturer.objects.count()
        )

        # Check session increment
        self.assertIn("num_visits", self.client.session)
        initial_visits = self.client.session["num_visits"]
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(self.client.session["num_visits"], initial_visits + 1)

        # Check template usage
        self.assertTemplateUsed(response, "taxi/index.html")


class ToggleAssignToCarTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(username="testdriver", password="testpassword", license_number="ABC12345")
        self.manufacturer = Manufacturer.objects.create(name="TestManufacturer", country="TestCountry")
        self.car = Car.objects.create(model="TestCar", manufacturer=self.manufacturer)
        self.url = reverse("taxi:toggle-car-assign", args=[self.car.pk])

    def test_toggle_assign_to_car(self):
        """
        ToggleAssignToCarTest:
        Test the behavior of the toggle_assign_to_car function.
        """
        self.client = Client()
        self.client.force_login(self.driver)

        # Initially, the driver should not be assigned to the car
        self.assertFalse(self.car in self.driver.cars.all())
        response = self.client.get(self.url)

        # After the toggle_assign_to_car view is called, the driver should be assigned to the car
        self.assertTrue(self.car in self.driver.cars.all())
        response = self.client.get(self.url)

        # After the second toggle_assign_to_car view call, the driver should be removed from the car
        self.assertFalse(self.car in self.driver.cars.all())

        # Check if the response redirects to the correct URL
        self.assertRedirects(response, reverse("taxi:car-detail", args=[self.car.pk]))
