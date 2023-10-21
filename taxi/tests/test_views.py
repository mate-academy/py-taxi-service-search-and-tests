from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")
INDEX_URL = reverse("taxi:index")
TOGGLE_ASSIGN_URL = "taxi:toggle-car-assign"


class PublicAccessTest(TestCase):
    def test_manufacturer_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_index_login_required(self):
        response = self.client.get(INDEX_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateAccessTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test1234",
            license_number="AAA66666"
        )
        self.client.force_login(self.user)

        test_manufacturer_1 = Manufacturer.objects.create(
            name="TestName1", country="TestCountry1"
        )
        test_manufacturer_2 = Manufacturer.objects.create(
            name="TestName2", country="TestCountry2"
        )

        Car.objects.create(
            model="TestModel1",
            manufacturer=test_manufacturer_1
        )
        Car.objects.create(
            model="TestModel2",
            manufacturer=test_manufacturer_2
        )

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)

        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_cars(self):
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)

        cars = Car.objects.all()
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )

        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)

        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers)
        )

        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_update_driver_license(self) -> None:
        new_license_number = "XYZ78910"
        url = reverse("taxi:driver-update", kwargs={"pk": self.user.pk})
        self.client.post(url, {"license_number": new_license_number})
        updated_driver = Driver.objects.get(pk=self.user.pk)
        self.assertEqual(updated_driver.license_number, new_license_number)


class SearchingTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test1234",
        )
        self.client.force_login(self.user)

        test_manufacturer_1 = Manufacturer.objects.create(
            name="TestName1", country="TestCountry1"
        )
        test_manufacturer_2 = Manufacturer.objects.create(
            name="TestName2", country="TestCountry2"
        )
        test_manufacturer_3 = Manufacturer.objects.create(
            name="TestManufacturer", country="TestCountry3"
        )

        Car.objects.create(
            model="TestModel1",
            manufacturer=test_manufacturer_1
        )
        Car.objects.create(
            model="TestModel2",
            manufacturer=test_manufacturer_2
        )
        Car.objects.create(
            model="TestCar3",
            manufacturer=test_manufacturer_3
        )

    def test_manufacturer_name_search(self):
        search_parameter = {"name": "TestName"}
        response = self.client.get(MANUFACTURER_URL, search_parameter)
        manufacturers = Manufacturer.objects.filter(
            name__icontains=search_parameter["name"]
        )

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_car_model_search(self):
        search_parameter = {"model": "TestModel"}
        response = self.client.get(CAR_URL, search_parameter)
        cars = Car.objects.filter(model__icontains=search_parameter["model"])
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )


class ToggleAssignToCarViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test", password="test123"
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(
            name="Audi", country="Germany"
        )
        self.car = Car.objects.create(model="A5", manufacturer=manufacturer)

    def test_toggle_assign_to_car_add(self):
        self.assertNotIn(self.car, self.user.cars.all())
        self.client.post(reverse(TOGGLE_ASSIGN_URL, args=[self.car.id]))
        self.assertIn(self.car, self.user.cars.all())

    def test_toggle_assign_to_car_remove(self):
        self.user.cars.add(self.car)
        self.client.post(reverse(TOGGLE_ASSIGN_URL, args=[self.car.id]))
        self.assertNotIn(self.car, self.user.cars.all())
