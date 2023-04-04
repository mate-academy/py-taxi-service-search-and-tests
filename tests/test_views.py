from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from taxi.forms import ManufacturerSearchForm
from taxi.models import Driver, Manufacturer, Car


class PublicAccessTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test"
        )
        self.driver = get_user_model().objects.create_user(
            username="testuser",
            password="12345"
        )
        self.car = Car.objects.create(
            model="testcar",
            manufacturer=self.manufacturer
        )

    def test_index(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertNotEqual(response.status_code, 200)

    def test_manufacturers_list(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertNotEqual(response.status_code, 200)

    def test_manufacturers_create(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))

        self.assertNotEqual(response.status_code, 200)

    def test_manufacturers_update(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-update",
            args=[self.manufacturer.pk]
        ))

        self.assertNotEqual(response.status_code, 200)

    def test_manufacturers_delete(self):
        response = self.client.get(reverse(
            "taxi:manufacturer-delete",
            args=[self.manufacturer.pk]
        ))

        self.assertNotEqual(response.status_code, 200)

    def test_cars_list(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertNotEqual(response.status_code, 200)

    def test_cars_detail(self):
        response = self.client.get(reverse(
            "taxi:car-detail",
            args=[self.car.pk]
        ))

        self.assertNotEqual(response.status_code, 200)

    def test_cars_create(self):
        response = self.client.get(reverse("taxi:car-create"))

        self.assertNotEqual(response.status_code, 200)

    def test_cars_update(self):
        response = self.client.get(reverse(
            "taxi:car-update",
            args=[self.car.pk]
        ))

        self.assertNotEqual(response.status_code, 200)

    def test_cars_delete(self):
        response = self.client.get(reverse(
            "taxi:car-delete",
            args=[self.car.pk]
        ))

        self.assertNotEqual(response.status_code, 200)

    def test_drivers_list(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertNotEqual(response.status_code, 200)

    def test_driver_detail(self):
        response = self.client.get(reverse(
            "taxi:driver-detail",
            args=[self.driver.pk]
        ))

        self.assertNotEqual(response.status_code, 200)

    def test_driver_create(self):
        response = self.client.get(reverse("taxi:driver-create"))

        self.assertNotEqual(response.status_code, 200)

    def test_drivers_delete(self):
        response = self.client.get(reverse(
            "taxi:driver-delete",
            args=[self.driver.pk]
        ))

        self.assertNotEqual(response.status_code, 200)

    def test_drivers_update(self):
        response = self.client.get(reverse(
            "taxi:driver-update",
            args=[self.driver.pk]
        ))

        self.assertNotEqual(response.status_code, 200)


class PrivateAccessTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test"
        )
        self.driver1 = get_user_model().objects.create_user(
            username="testuser1",
            password="12345",
            license_number="ABC12345"
        )

        self.driver2 = get_user_model().objects.create_user(
            username="testuser2",
            password="12345",
            license_number="ABC12346"
        )

        self.car = Car.objects.create(
            model="testcar",
            manufacturer=self.manufacturer
        )

        self.client.force_login(self.driver1)

    def test_driver_list(self):
        response = self.client.get(reverse("taxi:driver-list"))
        drivers_list = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers_list)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_detail(self):
        response = self.client.get(
            reverse("taxi:driver-detail", args=[self.driver1.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver1.username)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_driver_create(self):
        form_data = {
            "username": "testuser3",
            "password1": "user12345",
            "password2": "user12345",
            "first_name": "first",
            "last_name": "last",
            "license_number": "ABC12347",
        }
        self.client.post(
            reverse("taxi:driver-create"), form_data
        )
        driver = get_user_model().objects.get(username=form_data["username"])
        self.assertEqual(driver.username, form_data["username"])
        self.assertEqual(driver.first_name, form_data["first_name"])
        self.assertEqual(driver.last_name, form_data["last_name"])
        self.assertEqual(driver.license_number, form_data["license_number"])

    def test_driver_update_license(self):
        form_data = {"license_number": "BCV12345"}
        self.client.post(
            reverse(
                "taxi:driver-update",
                args=[self.driver1.pk]), data=form_data
        )
        driver = get_user_model().objects.get(pk=self.driver1.pk)
        self.assertEqual(driver.license_number, form_data["license_number"])

    def test_search_drivers_by_username(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "1"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "testuser2")

    def test_manufacturer_list(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        manufacturer_list = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer_list)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer_by_name(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "a"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "testmanufacturer2")

    def test_car_list(self):
        response = self.client.get(reverse("taxi:car-list"))
        car_list = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(car_list)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_detail(self):
        response = self.client.get(
            reverse("taxi:car-detail", args=[self.car.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.model)
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_search_car_by_model(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"model": "a"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "testcar2")


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("taxi:index")

        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="12345"
        )
        self.client.force_login(self.user)
        self.driver = Driver.objects.create(
            username="driver1",
            password="12345",
            license_number="ABC12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        self.car = Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer,
        )
        self.car.drivers.add(self.driver)

    def test_index_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to Best Taxi Ever!")
        self.assertContains(response, "Drivers")
        self.assertContains(response, "Cars")
        self.assertContains(response, "Manufacturers")
        self.assertContains(response, "You have visited this page")

    def test_index_view_without_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/accounts/login/?next={self.url}")


class ToggleAssignCarTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="Toyota")
        self.car = Car.objects.create(
            model="Camry",
            manufacturer=self.manufacturer
        )
        self.driver = get_user_model().objects.create_user(
            username="jon.doe",
            first_name="John",
            last_name="Doe",
            email="john@taxi.com",
            license_number="ABC12345"
        )
        self.driver.cars.add(self.car)

    def test_toggle_assign_to_car_view(self):
        self.client.login(username="testuser", password="password")
        url = reverse_lazy("taxi:toggle-car-assign", args=[self.car.pk])

        # Test assigning car to driver
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        # checking that user is in car.drivers
        self.car.refresh_from_db()
        self.assertIn(self.driver, self.car.drivers.all())

        # Test unassigning car from driver
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.driver.cars.filter(pk=self.car.pk).exists())
