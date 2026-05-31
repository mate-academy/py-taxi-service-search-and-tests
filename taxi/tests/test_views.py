from django.contrib.admin.templatetags.admin_list import search_form
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from taxi.models import Manufacturer, Car, Driver


class PublicManufacturerTest(TestCase):

    def test_login_required(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="Test_user123"
        )

        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        Manufacturer.objects.create(
            name="BYD",
            country="China"
        )

        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturers_list"]),
            list(manufacturers))
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="Eduardo",
            password="Ed123456")
        self.client.force_login(self.driver)

    def test_create_driver(self):
        form_data = {
            "username": "LeBronnnieJames",
            "password1": "Lbj12345_king",
            "password2": "Lbj12345_king",
            "first_name": "Lebron",
            "last_name": "James",
            "license_number": "LBJ12345"
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)

        new_driver = get_user_model().objects.get(
            username=form_data["username"])
        self.assertEqual(new_driver.first_name,
                         form_data["first_name"])
        self.assertEqual(new_driver.last_name,
                         form_data["last_name"])
        self.assertEqual(new_driver.license_number,
                         form_data["license_number"])


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user_2",
            password="Test_user123565"
        )

        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )

    def test_create_car(self):
        form_data = {
            "model": "Camry",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.user.id]
        }
        self.client.post(reverse("taxi:car-create"), data=form_data)

        created_car = Car.objects.get(model=form_data["model"])
        self.assertTrue(Car.objects.filter(model="Camry").exists())
        self.assertEqual(created_car.manufacturer.name, "Toyota")
        self.assertEqual(created_car.model, "Camry")
        self.assertEqual(created_car.drivers.count(), 1)


class ManufacturerSearchTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="Test_user123"
        )
        self.client.force_login(self.user)

        Manufacturer.objects.create(
            name="Renault",
            country="France"
        )

        Manufacturer.objects.create(
            name="Ferrari",
            country="Italy"
        )

        Manufacturer.objects.create(
            name="Ford",
            country="USA"
        )

    def test_search_returns_correct_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Ferrari"}
        )
        query = response.context["manufacturers_list"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(query.count(), 1)
        self.assertTrue(query.first().name, "Ferrari")

    def test_search_manufacturer_name_case_insensitive(self):
        response = self.client.get(reverse("taxi:manufacturer-list"),
                                   {"name": "fOrD"})
        query = response.context["manufacturers_list"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(query.count(), 1)
        self.assertEqual(query.first().name, "Ford")


class CarSearchTest(TestCase):
    def setUp(self):
        driver = get_user_model().objects.create_user(
            username="Eddie",
            password="Edd12345_"
        )
        self.client.force_login(driver)

        manufacturer = Manufacturer.objects.create(
            name="Ferrari",
            country="Italy"
        )

        car_1 = Car.objects.create(
            model="F40",
            manufacturer=manufacturer
        )

        car_2 = Car.objects.create(
            model="F80",
            manufacturer=manufacturer
        )
        car_1.drivers.add(driver)
        car_2.drivers.add(driver)

    def test_search_car_model_valid_search_data(self):
        response = self.client.get(reverse("taxi:car-list"),
                                   {"model": "f"})
        query = response.context["car_list"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(query.count(), 2)
        self.assertContains(response, "F40")
        self.assertContains(response, "F80")


class DriverSearchTest(TestCase):
    def setUp(self):
        driver = get_user_model().objects.create_user(
            username="JohnnyDepppp",
            password="Johnny123Ddd_"
        )
        self.client.force_login(driver)

    def test_search_driver_username_valid_search_data(self):
        response = self.client.get(reverse("taxi:driver-list"),
                                   {"username": "depp"})
        query = response.context["driver_list"]

        self.assertTrue(query.exists())
        self.assertEqual(query.count(), 1)
        self.assertEqual(query[0].username, "JohnnyDepppp")
