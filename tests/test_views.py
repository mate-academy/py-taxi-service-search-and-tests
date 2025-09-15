from pyexpat import model

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car


class IndexViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test User",
            password="Test Password",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertRedirects(
            response,
            f"/accounts/login/?next={reverse('taxi:index')}",
        )

    def test_index_view_logged_in_context_and_template(self):
        self.client.login(username="Test User", password="Test Password")
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)

        self.assertIn("num_drivers", response.context)
        self.assertIn("num_cars", response.context)
        self.assertIn("num_manufacturers", response.context)
        self.assertIn("num_visits", response.context)

        self.assertTemplateUsed(response, "taxi/index.html")

        first_visits = response.context["num_visits"]
        self.assertEqual(first_visits, 1)

        response2 = self.client.get(reverse("taxi:index"))
        second_visits = response2.context["num_visits"]
        self.assertEqual(second_visits, 2)


class ManufacturerViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test User",
            password="Test Password",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        Manufacturer.objects.create(name="Toyota", country="Japan")
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")
        Manufacturer.objects.create(name="Ford", country="USA")
        Manufacturer.objects.create(name="Honda", country="Japan")
        Manufacturer.objects.create(name="Kia", country="Korea")

    def test_manufacturer_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertRedirects(
            response,
            f"/accounts/login/?next={reverse('taxi:index')}",
        )

    def test_manufacturer_list_context_and_pagination(self):
        self.client.login(username="Test User", password="Test Password")
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("manufacturer_list", response.context)
        self.assertIn("search_form", response.context)

        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_manufacturer_list_filtering(self):
        self.client.login(username="Test User", password="Test Password")
        response = self.client.get(reverse("taxi:manufacturer-list")
                                   + "?name=Toyota")
        manufacturers = response.context["manufacturer_list"]
        self.assertEqual(len(manufacturers), 1)
        self.assertEqual(manufacturers[0].name, "Toyota")

    def test_manufacturer_create(self):
        self.client.login(username="Test User", password="Test Password")
        response = self.client.post(reverse("taxi:manufacturer-create"),
                                    {"name": "Tesla",
                                     "country": "USA",
                                     })
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertTrue(Manufacturer.objects.filter(name="Tesla",
                                                    country="USA").exists())

    def test_manufacturer_update(self):
        self.client.login(username="Test User", password="Test Password")
        response = self.client.post(reverse(
            "taxi:manufacturer-update", args=[self.manufacturer.id]), {
            "name": "Toyota Updated",
            "country": "Japan",
        })
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, "Toyota Updated")

    def test_manufacturer_delete(self):
        self.client.login(username="Test User", password="Test Password")
        manufacturer = Manufacturer.objects.get(name="Toyota")
        response = self.client.post(reverse(
            "taxi:manufacturer-delete", args=[manufacturer.id]))
        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertFalse(Manufacturer.objects.filter(name="Toyota").exists())


class CarViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test User",
            password="Test Password",
        )
        self.manufacturer1 = Manufacturer.objects.create(name="Toyota",
                                                         country="Japan")
        self.manufacturer2 = Manufacturer.objects.create(name="BMW",
                                                         country="Germany")
        self.manufacturer3 = Manufacturer.objects.create(name="Ford",
                                                         country="USA")

        self.car1 = Car.objects.create(model="Toyota Yaris",
                                       manufacturer=self.manufacturer1)
        self.car2 = Car.objects.create(model="BMW X5",
                                       manufacturer=self.manufacturer2)
        self.car3 = Car.objects.create(model="Ford Focus",
                                       manufacturer=self.manufacturer3)
        self.car4 = Car.objects.create(model="Toyota Corolla",
                                       manufacturer=self.manufacturer1)
        self.car5 = Car.objects.create(model="BMW 3 Series",
                                       manufacturer=self.manufacturer2)
        self.car6 = Car.objects.create(model="Ford Fiesta",
                                       manufacturer=self.manufacturer3)

    def test_car_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertRedirects(
            response,
            f"/accounts/login/?next={reverse('taxi:car-list')}",
        )

    def test_car_list_context_and_pagination(self):
        self.client.login(username="Test User", password="Test Password")
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("car_list", response.context)
        self.assertIn("search_form", response.context)

        self.assertEqual(len(response.context["car_list"]), 5)

    def test_car_list_filtering(self):
        self.client.login(username="Test User", password="Test Password")
        response = self.client.get(reverse("taxi:car-list")
                                   + "?model=Toyota Yaris")
        cars = response.context["car_list"]
        self.assertEqual(len(cars), 1)
        self.assertEqual(cars[0].model, "Toyota Yaris")

    def test_car_create(self):
        self.client.login(username="Test User", password="Test Password")
        response = self.client.post(reverse("taxi:car-create"),
                                    {
                                        "model": "BMW X6",
                                        "manufacturer": self.manufacturer2.id,
                                        "drivers": [self.user.id],
        })
        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertTrue(Car.objects.filter(
            model="BMW X6",
            manufacturer=self.manufacturer2).exists())

    def test_car_update(self):
        self.client.login(username="Test User", password="Test Password")
        response = self.client.post(reverse("taxi:car-update",
                                            args=[self.car1.id]),
                                    {
                                        "model": "Toyota Yaris Updated",
                                        "manufacturer": self.manufacturer2.id,
                                        "drivers": [self.user.id],
        })
        self.assertRedirects(response, reverse("taxi:car-list"))
        self.car1.refresh_from_db()
        self.assertEqual(self.car1.model, "Toyota Yaris Updated")

    def test_car_delete(self):
        self.client.login(username="Test User", password="Test Password")
        car = Car.objects.get(model="Toyota Yaris")
        response = self.client.post(reverse("taxi:car-delete",
                                            args=[car.id]))
        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertFalse(Car.objects.filter(model="Toyota Yaris").exists())


class DriverViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Test User",
            password="Test Password",
        )
        for i in range(10):
            get_user_model().objects.create_user(
                username=f"user{i}",
                password="12345",
                license_number=f"LIC{i}"
            )

    def test_driver_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertRedirects(
            response,
            f"/accounts/login/?next={reverse('taxi:driver-list')}",
        )

    def test_driver_list_context_and_pagination(self):
        self.client.login(username="Test User", password="Test Password")
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("driver_list", response.context)
        self.assertIn("search_form", response.context)
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_driver_list_filtering(self):
        self.client.login(username="Test User", password="Test Password")

        _ = get_user_model().objects.create_user(
            username="Alice",
            password="Test Password",
            license_number="Alice123"
        )

        response = self.client.get(reverse("taxi:driver-list")
                                   + "?username=Alice")
        self.assertEqual(response.status_code, 200)
        drivers = response.context["driver_list"]
        self.assertEqual(len(drivers), 1)
        self.assertEqual(drivers[0].username, "Alice")

    def test_driver_create(self):
        self.client.login(username="Test User", password="Test Password")
        driver = {
            "username": "Alice",
            "password1": "Complex!1234",
            "password2": "Complex!1234",
            "first_name": "Alice",
            "last_name": "Black",
            "license_number": "ALI12345",
        }

        response = self.client.post(reverse("taxi:driver-create"), data=driver)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("taxi:driver-list"))
        self.assertTrue(
            get_user_model().objects.filter(
                username="Alice",
                first_name="Alice",
                last_name="Black",
                license_number="ALI12345",
            ).exists()
        )
        user = get_user_model().objects.get(username="Alice")
        self.assertTrue(user.check_password("Complex!1234"))

    def test_driver_update(self):
        driver = get_user_model().objects.create_user(
            username="Alice",
            first_name="Alice",
            last_name="Black",
            license_number="ALI12345"
        )
        self.client.login(username="Test User", password="Test Password")
        response = self.client.post(reverse(
            "taxi:driver-update",
            args=[driver.id]), {
            "username": "Alice",
            "first_name": "Alice",
            "last_name": "Black",
            "license_number": "ALI54321"
        })
        self.assertRedirects(response, reverse("taxi:driver-list"))
        driver.refresh_from_db()
        self.assertEqual(driver.license_number, "ALI54321")

    def test_driver_delete(self):
        driver = get_user_model().objects.create_user(
            username="Alice",
            first_name="Alice",
            last_name="Black",
            license_number="ALI12345"
        )
        self.client.login(username="Test User", password="Test Password")
        response = self.client.post(reverse(
            "taxi:driver-delete",
            args=[driver.id]
        ))
        self.assertRedirects(response, reverse("taxi:driver-list"))
        self.assertFalse(
            get_user_model().objects.filter(id=driver.id).exists())


class ToggleAssignToCarTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="Test User",
            password="Test Password",
            license_number="ALI12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="Test Country",
        )
        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=self.manufacturer,
        )
        self.client = Client()
        self.client.login(username="Test User", password="Test Password")

    def test_toggle_assign_to_car_add_and_remove(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.id])
        response = self.client.get(url)
        self.driver.refresh_from_db()
        self.assertIn(self.car, self.driver.cars.all())
        self.assertEqual(response.status_code, 302)

        response = self.client.post(url)
        self.driver.refresh_from_db()
        self.assertNotIn(self.car, self.driver.cars.all())
        self.assertEqual(response.status_code, 302)
