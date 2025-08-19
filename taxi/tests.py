from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


class TestDriverModel(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="test.user",
            password="test1234",
            first_name="Vasya",
            last_name="Pupkin",
            license_number="ABC12345"
        )

    def test_str(self):
        self.assertEqual(str(self.driver), "test.user (Vasya Pupkin)")

    def test_absolute_url(self):
        expected_url = reverse(
            "taxi:driver-detail", kwargs={"pk": self.driver.pk}
        )
        self.assertEqual(self.driver.get_absolute_url(), expected_url)


class DriverCreateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Driver.objects.create_user(
            username="admin",
            password="adminpass",
            license_number="ADM12123"
        )
        self.client.login(username="admin", password="adminpass")

    def test_driver_create_view_post(self):
        url = reverse("taxi:driver-create")
        data = {
            "username": "vovas",
            "password1": "1234!@#$",
            "password2": "1234!@#$",
            "first_name": "vasya",
            "last_name": "pupkin",
            "license_number": "TST12345",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        driver = Driver.objects.get(username="vovas")
        self.assertEqual(driver.license_number, "TST12345")

    def test_driver_invalid_license(self):
        url = reverse("taxi:driver-create")
        data = {
            "username": "vovas",
            "password1": "1234!@#$",
            "password2": "1234!@#$",
            "first_name": "vasya",
            "last_name": "pupkin",
            "license_number": "TST1234",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_driver_invalid_password(self):
        url = reverse("taxi:driver-create")
        data = {
            "username": "vovas",
            "password1": "1234",
            "password2": "1234",
            "first_name": "vasya",
            "last_name": "pupkin",
            "license_number": "TST12345",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


class TestUpdateLicense(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Driver.objects.create_user(
            username="admin",
            password="adminpass",
            license_number="ADM12123"
        )
        self.client.login(username="admin", password="adminpass")

    def test_correct_license(self):
        self.driver = Driver.objects.create_user(
            username="vova",
            password="vova1234",
            license_number="ABC12345"
        )
        url = reverse("taxi:driver-update", kwargs={"pk": self.driver.pk})
        data = {"license_number": "TST54321"}
        response = self.client.post(url, data)
        self.driver.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.driver.license_number, "TST54321")

    def test_invalid_license(self):
        self.driver = Driver.objects.create_user(
            username="vova",
            password="vova1234",
            license_number="ABC12345"
        )
        url = reverse("taxi:driver-update", kwargs={"pk": self.driver.pk})
        data = {"license_number": "TS54321"}
        response = self.client.post(url, data)
        self.driver.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(self.driver.license_number, "TST54321")


class TestManufacturerSearch(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Driver.objects.create_user(
            username="admin",
            password="adminpass",
            license_number="ADM12123"
        )
        self.client.login(username="admin", password="adminpass")
        self.manufacturer1 = Manufacturer.objects.create(
            name="test1", country="UA"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="test2", country="USA"
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="test3", country="JA"
        )

    def test_no_search_parameters(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            [self.manufacturer1, self.manufacturer2, self.manufacturer3],
            ordered=False
        )

    def test_search_parameters(self):
        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "test1"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["manufacturer_list"],
            [self.manufacturer1]
        )


class TestCarSearch(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Driver.objects.create_user(
            username="admin",
            password="adminpass",
            license_number="ADM12123"
        )
        self.client.login(username="admin", password="adminpass")

        self.manufacturer1 = Manufacturer.objects.create(
            name="Nissan", country="Ja"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Dodge", country="USA"
        )
        self.manufacturer3 = Manufacturer.objects.create(
            name="Honda", country="JA"
        )

        self.car1 = Car.objects.create(
            model="Nissan Laurel", manufacturer=self.manufacturer1
        )
        self.car2 = Car.objects.create(
            model="Dodge Viper", manufacturer=self.manufacturer2
        )
        self.car3 = Car.objects.create(
            model="Honda Civic ek9 1999 Type R ",
            manufacturer=self.manufacturer3
        )

    def test_no_search_parameters(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertQuerysetEqual(
            response.context["car_list"],
            [self.car1, self.car2, self.car3],
            ordered=False
        )

    def test_search_parameters(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "Honda Civic"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["car_list"],
            [self.car3]
        )


class TestDriverSearch(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Driver.objects.create_user(
            username="admin",
            password="adminpass",
            license_number="ADM12123"
        )
        self.client.login(username="admin", password="adminpass")
        self.driver1 = Driver.objects.create_user(
            username="vova", password="1234", license_number="AAA11111"
        )
        self.driver2 = Driver.objects.create_user(
            username="bogdan", password="1234", license_number="BBB22222"
        )
        self.driver3 = Driver.objects.create_user(
            username="gleb", password="1234", license_number="CCC33333"
        )

    def test_no_search_parameters(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertQuerysetEqual(
            response.context["driver_list"],
            [self.user, self.driver1, self.driver2, self.driver3],
            ordered=False,
        )

    def test_search_parameters(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "vov"})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context["driver_list"],
            [self.driver1]
        )
