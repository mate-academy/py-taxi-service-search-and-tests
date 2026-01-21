from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer, Driver

DRIVER_URL = reverse("taxi:driver-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")


class CarListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user", password="password123"
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Audi",
            country="Germany"
        )
        Car.objects.create(model="Test1", manufacturer=self.manufacturer)
        Car.objects.create(model="Test2", manufacturer=self.manufacturer)
        Car.objects.create(model="Test3", manufacturer=self.manufacturer)

    def test_car_list_view_status_code(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)

    def test_car_list_view_template_used(self):
        response = self.client.get(CAR_URL)
        self.assertTemplateUsed(response, "taxi/car_list.html")


class PublicDriverTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DRIVER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.driver = Driver.objects.create(
            username="test_name",
            password="password123",
            license_number="QWE12345",
        )
        self.update_url = reverse("taxi:driver-update", args=[self.driver.id])

    def test_retrieve_drivers(self):
        Driver.objects.create(
            username="driver1", password="password1", license_number="ADA12345"
        )
        Driver.objects.create(
            username="driver2", password="password2", license_number="ADA67890"
        )

        response = self.client.get(DRIVER_URL)

        self.assertEqual(response.status_code, 200)
        drivers = Driver.objects.all()
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_create_driver(self):
        form_data = {
            "username": "newdriver",
            "password1": "newpassword123",
            "password2": "newpassword123",
            "license_number": "XYZ98765",
        }
        response = self.client.post(
            reverse("taxi:driver-create"),
            data=form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Driver.objects.filter(username="newdriver").exists())

    def test_update_driver_view(self):
        form_data = {
            "license_number": "UPD12345",
        }
        response = self.client.post(self.update_url, data=form_data)
        self.assertRedirects(response, DRIVER_URL)
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.license_number, "UPD12345")


class IndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        Car.objects.create(model="Corolla", manufacturer=manufacturer)

    def setUp(self):
        self.client.login(username="testuser", password="testpassword")

    def test_index_view_status_code(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)

    def test_index_view_context(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.context["num_drivers"], 1)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_manufacturers"], 1)
        self.assertEqual(response.context["num_visits"], 1)


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Old Name", country="Old Country"
        )

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="BMW", country="Germany")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_create_manufacturer(self):
        form_data = {"name": "Ford", "country": "USA"}
        response = self.client.post(
            reverse("taxi:manufacturer-create"),
            data=form_data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Manufacturer.objects.filter(name="Ford").exists())

    def test_update_manufacturer_view(self):
        form_data = {"name": "Updated Name", "country": "Updated Country"}
        response = self.client.post(
            reverse("taxi:manufacturer-update", args=[self.manufacturer.id]),
            data=form_data,
        )
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, "Updated Name")
        self.assertEqual(self.manufacturer.country, "Updated Country")

    def test_delete_manufacturer(self):
        response = self.client.post(
            reverse("taxi:manufacturer-delete", args=[self.manufacturer.id])
        )
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertFalse(
            Manufacturer.objects.filter(id=self.manufacturer.id).exists()
        )
