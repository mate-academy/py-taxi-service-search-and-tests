from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Manufacturer, Driver, Car
from .forms import (
    DriverCreationForm,
    DriverLicenseUpdateForm,
    ManufacturerNameSearchForm,
    CarModelSearchForm,
    DriversUsernameSearchForm,
)


class ManufacturerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="Ford", country="USA")

    def test_string_representation(self):
        manufacturer = Manufacturer.objects.get(name="Toyota")
        self.assertEqual(str(manufacturer), "Toyota Japan")

    def test_ordering(self):
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(list(manufacturers),
                         list(manufacturers.order_by("name")))


class DriverModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create_user(
            username="testdriver",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
            password="secret"
        )

    def test_string_representation(self):
        driver = Driver.objects.get(username="testdriver")
        expected = (
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )
        self.assertEqual(str(driver), expected)

    def test_license_number_validation(self):
        driver = Driver.objects.get(username="testdriver")
        self.assertEqual(driver.license_number, "ABC12345")


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="Honda", country="Japan"
        )
        driver = get_user_model().objects.create_user(
            username="drivercar",
            license_number="XYZ98765",
            first_name="Jane",
            last_name="Smith",
            password="secret"
        )
        car = Car.objects.create(model="Civic", manufacturer=manufacturer)
        car.drivers.add(driver)

    def test_string_representation(self):
        car = Car.objects.get(model="Civic")
        self.assertEqual(str(car), "Civic")

    def test_manufacturer_relationship(self):
        car = Car.objects.get(model="Civic")
        self.assertEqual(car.manufacturer.name, "Honda")

    def test_drivers_relationship(self):
        car = Car.objects.get(model="Civic")
        self.assertEqual(car.drivers.count(), 1)
        self.assertEqual(car.drivers.first().username, "drivercar")


class FormTests(TestCase):
    def test_manufacturer_search_form_valid(self):
        form = ManufacturerNameSearchForm(data={"name": "toy"})
        self.assertTrue(form.is_valid())

    def test_manufacturer_search_form_blank(self):
        form = ManufacturerNameSearchForm(data={"name": ""})
        self.assertTrue(form.is_valid())

    def test_car_search_form_valid(self):
        form = CarModelSearchForm(data={"model": "civic"})
        self.assertTrue(form.is_valid())

    def test_driver_search_form_valid(self):
        form = DriversUsernameSearchForm(data={"username": "john"})
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_valid(self):
        form = DriverCreationForm(data={
            "username": "newdriver",
            "license_number": "AAA11111",
            "first_name": "First",
            "last_name": "Last",
            "password1": "securepassword123",
            "password2": "securepassword123",
        })
        self.assertTrue(form.is_valid())

    def test_driver_license_update_form_valid(self):
        driver = get_user_model().objects.create_user(
            username="licenseup",
            license_number="BBB22222",
            first_name="Fn",
            last_name="Ln",
            password="pass"
        )
        form = DriverLicenseUpdateForm(
            instance=driver,
            data={"license_number": "CCC33333"},
        )
        self.assertTrue(form.is_valid())


class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer1 = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        cls.manufacturer2 = Manufacturer.objects.create(
            name="Ford", country="USA"
        )
        cls.driver1 = get_user_model().objects.create_user(
            username="driver1",
            license_number="AAA11111",
            first_name="Anna",
            last_name="Smith",
            password="secret"
        )
        cls.driver2 = get_user_model().objects.create_user(
            username="driver2",
            license_number="BBB22222",
            first_name="Bob",
            last_name="Jones",
            password="secret"
        )
        cls.car1 = Car.objects.create(
            model="Corolla", manufacturer=cls.manufacturer1
        )
        cls.car1.drivers.add(cls.driver1)
        cls.car2 = Car.objects.create(
            model="Mustang", manufacturer=cls.manufacturer2
        )
        cls.car2.drivers.add(cls.driver2)
        cls.car3 = Car.objects.create(
            model="Focus", manufacturer=cls.manufacturer2
        )
        cls.car3.drivers.add(cls.driver1, cls.driver2)

    def setUp(self):
        self.client.login(username=self.driver1.username, password="secret")

    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cars:")
        self.assertContains(response, "Drivers:")
        self.assertContains(response, "Manufacturers:")
        self.assertContains(response, "<strong>Cars:</strong> 3")
        self.assertContains(response, "<strong>Drivers:</strong> 2")
        self.assertContains(response, "<strong>Manufacturers:</strong> 2")

    def test_manufacturer_list_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer1.name)
        self.assertContains(response, self.manufacturer2.name)
        self.assertEqual(len(response.context["manufacturer_list"]), 2)

    def test_manufacturer_list_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=yot"
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manufacturer1.name)
        self.assertNotContains(response, self.manufacturer2.name)
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=ford"
        )
        self.assertContains(response, self.manufacturer2.name)
        self.assertNotContains(response, self.manufacturer1.name)

    def test_car_list_view(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car1.model)
        self.assertContains(response, self.car2.model)
        self.assertContains(response, self.car3.model)
        self.assertEqual(len(response.context["car_list"]), 3)

    def test_car_list_search(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=corolla")
        self.assertContains(response, self.car1.model)
        self.assertNotContains(response, self.car2.model)
        self.assertNotContains(response, self.car3.model)

        response = self.client.get(reverse("taxi:car-list") + "?model=mustang")
        self.assertContains(response, self.car2.model)
        self.assertNotContains(response, self.car1.model)
        self.assertNotContains(response, self.car3.model)

    def test_driver_list_view(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver1.username)
        self.assertContains(response, self.driver2.username)
        self.assertEqual(len(response.context["driver_list"]), 2)

    def test_driver_list_search(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=driver1"
        )
        self.assertContains(response, '<td><a href="/drivers/1/">driver1')
        self.assertNotContains(response, '<td><a href="/drivers/2/">driver2')

        response = self.client.get(
            reverse("taxi:driver-list") + "?username=driver2"
        )
        self.assertContains(response, '<td><a href="/drivers/2/">driver2')
        self.assertNotContains(response, '<td><a href="/drivers/1/">driver1')

    def test_toggle_assign_to_car_view(self):
        self.assertNotIn(self.car2, self.driver1.cars.all())
        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car2.id])
        )
        self.assertRedirects(
            response,
            reverse("taxi:car-detail", args=[self.car2.id])
        )
        self.driver1.refresh_from_db()
        self.assertIn(self.car2, self.driver1.cars.all())
        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car2.id])
        )
        self.assertRedirects(
            response,
            reverse("taxi:car-detail", args=[self.car2.id])
        )
        self.driver1.refresh_from_db()
        self.assertNotIn(self.car2, self.driver1.cars.all())

    def test_manufacturer_create_view(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            {
                "name": "Tesla",
                "country": "USA",
            },
        )
        self.assertRedirects(
            response,
            reverse("taxi:manufacturer-list")
        )
        self.assertTrue(Manufacturer.objects.filter(name="Tesla").exists())

    def test_manufacturer_update_view(self):
        response = self.client.get(
            reverse("taxi:manufacturer-update", args=[self.manufacturer1.id])
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("taxi:manufacturer-update", args=[self.manufacturer1.id]),
            {"name": "Toyota Updated", "country": "Japan"}
        )
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.manufacturer1.refresh_from_db()
        self.assertEqual(self.manufacturer1.name, "Toyota Updated")

    def test_manufacturer_delete_view(self):
        response = self.client.get(
            reverse("taxi:manufacturer-delete", args=[self.manufacturer2.id])
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            reverse("taxi:manufacturer-delete", args=[self.manufacturer2.id])
        )
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertFalse(
            Manufacturer.objects.filter(id=self.manufacturer2.id).exists()
        )
