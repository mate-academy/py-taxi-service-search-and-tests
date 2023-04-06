from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

DRIVER_URL = reverse("taxi:driver-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")

class PublicViewsLoginRequiredTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="Test",
            country="Test"
        )
        cls.driver = get_user_model().objects.create_user(
            username="test",
            password="StrongPass1"
        )
        cls.car = Car.objects.create(
            model="test",
            manufacturer=cls.manufacturer,
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


class PrivateDriverTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create_user(
            username="test",
            password="StrongPass1",
            license_number="ABC12345"
        )
        cls.user2 = get_user_model().objects.create_user(
            username="test2",
            password="StrongPass1",
            license_number="ABC12346"
        )

    def setUp(self) -> None:
        self.client.force_login(self.user1)

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
            reverse("taxi:driver-detail", args=[self.user1.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user1.username)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_driver_create(self):
        form_data = {
            "username": "test3",
            "password1": "StrongPass1",
            "password2": "StrongPass1",
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
            reverse("taxi:driver-update", args=[self.user1.pk]), data=form_data
        )
        driver = get_user_model().objects.get(pk=self.user1.pk)
        self.assertEqual(driver.license_number, form_data["license_number"])

    def test_search_driver(self):
        Driver.objects.create(
            username="Test",
            password="1876545",
            license_number="LOM54572"
        )
        Driver.objects.create(
            username="Test2",
            password="987654325",
            license_number="GOI76545"
        )
        response = self.client.get(DRIVER_URL)
        drivers = Driver.objects.filter(username__icontains="e")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )
        for driver in response.context["driver_list"]:
            self.assertIn("e", driver.username)


class PrivateManufacturerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer1 = Manufacturer.objects.create(
            name="manufacturer1",
            country="manufacturer1"
        )
        cls.manufacturer1 = Manufacturer.objects.create(
            name="manufacturer2",
            country="manufacturer2"
        )
        cls.user1 = get_user_model().objects.create_user(
            username="test",
            password="StrongPass1",
            license_number="ABC12345"
        )

    def setUp(self) -> None:
        self.client.force_login(self.user1)

    def test_manufacturer_list(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        manufacturer_list = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer_list)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateCarTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(
            name="manufacturer2",
            country="manufacturer2"
        )
        cls.car1 = Car.objects.create(
            model="test1",
            manufacturer=cls.manufacturer
        )
        cls.car2 = Car.objects.create(
            model="test2",
            manufacturer=cls.manufacturer
        )
        cls.user = get_user_model().objects.create_user(
            username="test",
            password="StrongPass1",
            license_number="ABC12345"
        )

    def setUp(self) -> None:
        self.client.force_login(self.user)

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
            reverse("taxi:car-detail", args=[self.car1.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car1.model)
        self.assertTemplateUsed(response, "taxi/car_detail.html")


class PublicCarTest(TestCase):
    def test_login_required(self):
        res = self.client.get(CAR_URL)

        self.assertNotEqual(res.status_code, 200)

    def test_toggle_assign_to_car(self):
        manufacturer = Manufacturer.objects.create(
            name="Honda",
            country="Japan"
        )
        car = Car.objects.create(
            model="CR-V",
            manufacturer=manufacturer
        )
        driver = get_user_model().objects.create_user(
            "Paula",
            "dfg543sd4tyfE"
        )
        self.client.force_login(driver)
        response = self.client.post(
            reverse("taxi:toggle-car-assign", args=[car.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(car in driver.cars.all())

        response = self.client.post(
            reverse("taxi:toggle-car-assign", args=[car.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(car in driver.cars.all())

