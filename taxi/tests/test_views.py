from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

CAR_LIST_URL = reverse("taxi:car-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicAccessTests(TestCase):
    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer", country="Test Country"
        )
        self.driver = get_user_model().objects.create_user(
            username="testdriver",
            password="test_password123",
            license_number="AB12345",
        )
        self.car = Car.objects.create(
            model="Test Car", manufacturer=self.manufacturer
        )

    def test_login_required_car_list(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 302)

    def test_login_required_driver_list(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 302)

    def test_login_required_manufacturer_list(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 302)

    def test_login_required_car_detail(self):
        response = self.client.get(
            reverse("taxi:car-detail", args=[self.car.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_login_required_driver_detail(self):
        response = self.client.get(
            reverse("taxi:driver-detail", args=[self.driver.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_login_required_car_update(self):
        response = self.client.get(
            reverse("taxi:car-update", args=[self.car.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_login_required_driver_update(self):
        response = self.client.get(
            reverse("taxi:driver-update", args=[self.driver.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_login_required_manufacturer_update(self):
        response = self.client.get(
            reverse("taxi:manufacturer-update", args=[self.manufacturer.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_login_required_car_delete(self):
        response = self.client.get(
            reverse("taxi:car-delete", args=[self.car.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_login_required_driver_delete(self):
        response = self.client.get(
            reverse("taxi:driver-delete", args=[self.driver.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_login_required_car_create(self):
        resource = self.client.get(reverse("taxi:car-create"))
        self.assertEqual(resource.status_code, 302)

    def test_login_required_driver_create(self):
        resource = self.client.get(reverse("taxi:driver-create"))
        self.assertEqual(resource.status_code, 302)


class PrivateAccessTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Ford", country="USA"
        )
        self.user = get_user_model().objects.create_user(
            username="coconut",
            password="POoi274**",
            license_number="ABC12345",
        )
        self.car = Car.objects.create(
            model="Focus",
            manufacturer=self.manufacturer,
        )
        self.driver = get_user_model().objects.create_user(
            username="clevford",
            password="JHyf67$",
            license_number="ABT12345",
        )
        self.client.force_login(self.user)

    def test_login_required_car_list(self):
        response = self.client.get(CAR_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_login_required_driver_list(self):
        response = self.client.get(DRIVER_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_login_required_manufacturer_list(self):
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(response.status_code, 200)

    def test_login_required_car_detail(self):
        response = self.client.get(
            reverse("taxi:car-detail", args=[self.car.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_login_required_driver_detail(self):
        response = self.client.get(
            reverse("taxi:driver-detail", args=[self.driver.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_login_required_car_update(self):
        response = self.client.get(
            reverse("taxi:car-update", args=[self.car.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_login_required_driver_update(self):
        response = self.client.get(
            reverse("taxi:driver-update", args=[self.driver.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_login_required_manufacturer_update(self):
        response = self.client.get(
            reverse("taxi:manufacturer-update", args=[self.manufacturer.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_login_required_car_delete(self):
        response = self.client.get(
            reverse("taxi:car-delete", args=[self.car.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_login_required_driver_delete(self):
        response = self.client.get(
            reverse("taxi:driver-delete", args=[self.driver.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_login_required_car_create(self):
        resource = self.client.get(reverse("taxi:car-create"))
        self.assertEqual(resource.status_code, 200)

    def test_login_required_driver_create(self):
        resource = self.client.get(reverse("taxi:driver-create"))
        self.assertEqual(resource.status_code, 200)


class SearchFunctionalityTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testdriver1",
            password="test_password123",
            license_number="ABG12345",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Jeep", country="USA"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Toyota", country="Japan"
        )
        self.driver1 = get_user_model().objects.create_user(
            username="piccolo",
            license_number="JYU67485",
            first_name="John",
            last_name="Doe",
        )
        self.driver2 = get_user_model().objects.create_user(
            username="ragingbull",
            license_number="CD67890",
            first_name="Jane",
            last_name="Smith",
        )
        self.car1 = Car.objects.create(
            model="Wrangler", manufacturer=self.manufacturer
        )
        self.car2 = Car.objects.create(
            model="Cherokee", manufacturer=self.manufacturer
        )
        self.car1.drivers.add(self.driver1)
        self.car2.drivers.add(self.driver2)
        self.client.force_login(self.user)

    def test_driver_search(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "piccolo"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "piccolo")
        self.assertNotContains(response, "ragingbull")

    def test_car_search(self):
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Wrangler"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wrangler")
        self.assertNotContains(response, "Cherokee")

    def test_manufacturer_search(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Jeep"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jeep")
        self.assertNotContains(response, "Toyota")


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testdriver1",
            password="test_password123",
            license_number="ABG12345",
        )

        self.client.force_login(self.user)

    def test_manufacturer_list(self):
        Manufacturer.objects.create(name="Fiat", country="Italy")
        Manufacturer.objects.create(name="Renault", country="France")

        manufacturers = Manufacturer.objects.all()
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["object_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")


class PrivateCarTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testdriver1",
            password="test_password123",
            license_number="ABG12345",
        )

        self.client.force_login(self.user)

    def test_car_list(self):
        manufacturer1 = Manufacturer.objects.create(
            name="Ferrari", country="Italy"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="BMW", country="Germany"
        )
        Car.objects.create(model="458 Spider", manufacturer=manufacturer1)
        Car.objects.create(model="i8", manufacturer=manufacturer2)

        cars = Car.objects.all()
        response = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["object_list"]),
            list(cars),
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_detail(self):
        manufacturer = Manufacturer.objects.create(
            name="Daewoo", country="Korea"
        )
        car = Car.objects.create(model="Nexia", manufacturer=manufacturer)

        response = self.client.get(reverse("taxi:car-detail", args=[car.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["object"],
            car,
        )
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    class PrivateDriverTests(TestCase):
        def setUp(self):
            self.user = get_user_model().objects.create_user(
                username="testdriver1",
                password="test_password123",
                license_number="ABG12345",
            )

        def test_driver_list(self):
            Driver.objects.create(
                username="piccolo",
                password="tEst_passwfdsfdsord123()(",
                license_number="JYU67485",
            )

            drivers = Driver.objects.all()
            response = self.client.get(reverse("taxi:driver-list"))

            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                list(response.context["object_list"]),
                list(drivers),
            )
            self.assertTemplateUsed(response, "taxi/driver_list.html")

        def test_driver_detail(self):
            driver = Driver.objects.create(
                username="fdsfdsfsaf",
                password="tEst_passwfdsfdsord1432432sdca3()(",
                license_number="JYU67485",
            )

            response = self.client.get(
                reverse("taxi:driver-detail", args=[driver.pk])
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.context["object"],
                driver,
            )
            self.assertTemplateUsed(response, "taxi/driver_detail.html")

        def test_toggle_assign_to_car(self):
            manufacturer = Manufacturer.objects.create(
                name="Honda", country="Japan"
            )
            car = Car.objects.create(model="Accord", manufacturer=manufacturer)

            response = self.client.get(
                reverse("taxi:toggle-assign-to-car", args=[car.pk])
            )
            driver_cars = self.user.cars.all()

            self.assertEqual(response.status_code, 200)
            self.assertContains(driver_cars, car)
