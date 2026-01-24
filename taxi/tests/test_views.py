from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")
INDEX_URL = reverse("taxi:index")


class LoginMixin:

    def setUp(self):
        super().setUp()

        self.driver = get_user_model().objects.create_user(
            username="john_test",
            password="test123",
            license_number="FFF00000"
        )
        self.client.force_login(self.driver)


class LogoutIndexPageTests(TestCase):

    def test_login_required(self):
        login_url = settings.LOGIN_URL
        response = self.client.get(INDEX_URL)
        self.assertRedirects(
            response,
            f"{login_url}?next={INDEX_URL}"
        )


class LoginIndexPageTests(LoginMixin, TestCase):

    def test_index_for_displaying_context_and_counters(self):
        response = self.client.get(INDEX_URL)

        self.assertIn("num_drivers", response.context)
        self.assertIn("num_cars", response.context)
        self.assertIn("num_manufacturers", response.context)
        self.assertIn("num_visits", response.context)

        self.assertEqual(
            response.context["num_drivers"],
            Driver.objects.count()
        )
        self.assertEqual(
            response.context["num_cars"],
            Car.objects.count()
        )
        self.assertEqual(
            response.context["num_manufacturers"],
            Manufacturer.objects.count()
        )

        initial_visit = response.context["num_visits"]
        response2 = self.client.get(INDEX_URL)
        self.assertEqual(response2.context["num_visits"], initial_visit + 1)


class LogoutManufacturerListTests(TestCase):

    def test_login_required(self):
        login_url = settings.LOGIN_URL
        response = self.client.get(MANUFACTURER_URL)
        self.assertRedirects(response, f"{login_url}?next={MANUFACTURER_URL}")


class LoginManufacturerListTest(LoginMixin, TestCase):

    def setUp(self):
        super().setUp()

        number_of_manufacturer = 7

        for manufacturer_id in range(number_of_manufacturer):
            Manufacturer.objects.create(
                name=f"Test - {manufacturer_id}",
                country=f"TestUA - {manufacturer_id}",
            )

    def test_login_manufacturer(self):
        response = self.client.get(MANUFACTURER_URL)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

        response2 = self.client.get(MANUFACTURER_URL + "?page=2")
        self.assertEqual(len(response2.context["manufacturer_list"]), 2)

    def test_get_context_with_search_form(self):
        response = self.client.get(MANUFACTURER_URL + "?name=BMW")

        self.assertIn("search_form", response.context)

        form = response.context["search_form"]
        self.assertEqual(form.initial["name"], "BMW")

    def test_get_queryset_filter(self):

        Manufacturer.objects.create(name="Toyota", country="DU")
        Manufacturer.objects.create(name="Toyota2", country="DU")

        response = self.client.get(MANUFACTURER_URL + "?name=Toy")
        qs = response.context["manufacturer_list"]
        names = [m.name for m in qs]

        self.assertEqual(len(qs), 2)
        self.assertIn("Toyota", names)
        self.assertIn("Toyota2", names)


class LogoutManufacturerCDUTest(TestCase):

    def test_login_required(self):
        login_url = settings.LOGIN_URL
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertRedirects(
            response,
            f"{login_url}?next={reverse('taxi:manufacturer-create')}"
        )


class LoginManufacturerCDUTest(LoginMixin, TestCase):

    def test_manufacturer_create(self):

        create_url = reverse("taxi:manufacturer-create")
        data = {
            "name": "BMW",
            "country": "DL"
        }

        response = self.client.post(create_url, data=data)
        self.assertRedirects(response, MANUFACTURER_URL)

        manufacturer = Manufacturer.objects.get(name="BMW")
        self.assertEqual(manufacturer.country, "DL")

    def test_manufacturer_update(self):

        manufacturer = Manufacturer.objects.create(
            name="Odl",
            country="Old.old"
        )
        data = {
            "name": "New",
            "country": "New.new"
        }
        update_url = reverse(
            "taxi:manufacturer-update",
            args=[manufacturer.id]
        )
        response = self.client.post(update_url, data=data)

        manufacturer.refresh_from_db()
        self.assertEqual(manufacturer.name, "New")
        self.assertRedirects(response, MANUFACTURER_URL)

    def test_manufacturer_delete(self):

        manufacturer = Manufacturer.objects.create(
            name="DeleteMe",
            country="DeleteMe"
        )
        delete_url = reverse(
            "taxi:manufacturer-delete",
            args=[manufacturer.id]
        )
        response = self.client.post(delete_url)

        self.assertEqual(Manufacturer.objects.count(), 0)
        self.assertRedirects(response, MANUFACTURER_URL)


class LogoutCarListTest(TestCase):

    def test_login_required(self):
        login_url = settings.LOGIN_URL
        response = self.client.get(CAR_URL)
        self.assertRedirects(response, f"{login_url}?next={CAR_URL}")


class LoginCarListTest(LoginMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="DU"
        )

        number_of_car = 7
        for car_id in range(number_of_car):
            Car.objects.create(
                model=f"Test - {car_id}",
                manufacturer=self.manufacturer,
            )

    def test_login_car_list_and_pagination(self):
        response = self.client.get(CAR_URL)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "taxi/car_list.html")

        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 5)

        response2 = self.client.get(CAR_URL + "?page=2")
        self.assertEqual(len(response2.context["car_list"]), 2)

    def test_car_get_context_with_search_form(self):
        response = self.client.get(CAR_URL + "?model=BMW")

        self.assertIn("search_form", response.context)

        form = response.context["search_form"]
        self.assertEqual(form.initial["model"], "BMW")

    def test_car_get_queryset_filter(self):

        Car.objects.create(model="Toyota", manufacturer=self.manufacturer)

        response = self.client.get(CAR_URL + "?model=Toy")
        qs = response.context["car_list"]
        models = [c.model for c in qs]

        self.assertEqual(len(qs), 1)
        self.assertIn("Toyota", models)

    def test_toggle_assign_to_car(self):

        driver = Driver.objects.get(pk=self.driver.id)
        car = Car.objects.get(model="Test - 0")

        self.assertNotIn(car, driver.cars.all())
        response = self.client.post(
            reverse("taxi:toggle-car-assign", args=[car.id])
        )

        driver.refresh_from_db()
        self.assertIn(car, driver.cars.all())
        self.assertRedirects(
            response,
            reverse("taxi:car-detail", args=[car.id])
        )


class LogoutCarCDUTest(TestCase):
    def test_login_required(self):
        login_url = settings.LOGIN_URL
        response = self.client.get(reverse("taxi:car-create"))
        self.assertRedirects(
            response,
            f"{login_url}?next={reverse('taxi:car-create')}"
        )


class LoginCarCDUTest(LoginMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="DL"
        )

    def test_car_create(self):

        create_url = reverse("taxi:car-create")

        data = {
            "model": "BMW",
            "manufacturer": self.manufacturer.id,
            "drivers": self.driver.id
        }

        response = self.client.post(create_url, data=data)
        self.assertRedirects(response, CAR_URL)

        car = Car.objects.get(model="BMW")
        self.assertEqual(car.manufacturer.country, "DL")

    def test_car_update(self):

        car = Car.objects.create(
            model="BMW", manufacturer=self.manufacturer
        )

        data = {
            "model": "NewBMW",
            "manufacturer": self.manufacturer.id,
            "drivers": self.driver.id
        }

        update_url = reverse(
            "taxi:car-update",
            args=[car.id]
        )
        response = self.client.post(update_url, data=data)

        car.refresh_from_db()
        self.assertEqual(car.model, "NewBMW")
        self.assertRedirects(response, CAR_URL)

    def test_car_delete(self):
        car = Car.objects.create(
            model="DeleteMe", manufacturer=self.manufacturer
        )
        delete_url = reverse("taxi:car-delete", args=[car.id])
        response = self.client.post(delete_url)

        self.assertEqual(Car.objects.count(), 0)
        self.assertRedirects(response, CAR_URL)


class LogoutDriverListTest(TestCase):
    def test_login_required(self):
        login_url = settings.LOGIN_URL
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertRedirects(
            response,
            f"{login_url}?next={reverse('taxi:driver-list')}"
        )


class LoginDriverListTest(LoginMixin, TestCase):

    def setUp(self):
        super().setUp()

        for i in range(7):
            Driver.objects.create_user(
                username=f"user{i}",
                password="12345test",
                license_number=f"ABG1111{i}"
            )

    def test_login_driver_list_and_pagination(self):
        response = self.client.get(DRIVER_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 5)

        response2 = self.client.get(DRIVER_URL + "?page=2")
        self.assertEqual(len(response2.context["driver_list"]), 3)

    def test_driver_get_context_with_search_form(self):
        response = self.client.get(DRIVER_URL + "?username=adm")

        self.assertIn("search_form", response.context)
        form = response.context["search_form"]
        self.assertEqual(form.initial["username"], "adm")

    def test_driver_get_queryset_filter(self):

        response = self.client.get(DRIVER_URL + "?username=user1")
        qs = response.context["driver_list"]

        usernames = [d.username for d in qs]

        self.assertEqual(len(qs), 1)
        self.assertIn("user1", usernames)


class LogoutDriverCDUTest(TestCase):
    def test_login_required(self):
        login_url = settings.LOGIN_URL
        url = reverse("taxi:driver-create")

        response = self.client.get(url)

        self.assertRedirects(
            response,
            f"{login_url}?next={url}"
        )


class LoginDriverCDUTest(LoginMixin, TestCase):

    def test_driver_create(self):
        url = reverse("taxi:driver-create")

        data = {
            "username": "newuser",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "license_number": "AAA00000"
        }

        response = self.client.post(url, data=data)
        driver = Driver.objects.get(username="newuser")
        self.assertRedirects(
            response, reverse("taxi:driver-detail", args=[driver.id])
        )
        self.assertIn(
            driver,
            Driver.objects.all()
        )

    def test_driver_update_license(self):
        driver = Driver.objects.create_user(
            username="testdriver",
            password="12345"
        )

        url = reverse("taxi:driver-update", args=[driver.id])

        data = {
            "license_number": "ABC12345"
        }

        response = self.client.post(url, data=data)

        driver.refresh_from_db()

        self.assertEqual(driver.license_number, "ABC12345")
        self.assertRedirects(response, reverse("taxi:driver-list"))

    def test_driver_delete(self):
        driver = Driver.objects.create_user(
            username="todelete",
            password="12345",
            license_number="DLT00012"
        )

        url = reverse("taxi:driver-delete", args=[driver.id])

        response = self.client.post(url)

        self.assertFalse(Driver.objects.filter(id=driver.id).exists())
        self.assertRedirects(response, reverse("taxi:driver-list"))
