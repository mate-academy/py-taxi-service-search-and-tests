from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_URL = reverse("taxi:manufacturer-create")
DRIVER_URL = reverse("taxi:driver-list")
CAR_URL = reverse("taxi:car-list")
TOGGLE_ASSIGN_URL = "taxi:toggle-car-assign"


class PublicTaxiServiceListsTest(TestCase):
    def test_driver_login_required(self) -> None:
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_login_required(self) -> None:
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)

    def test_car_login_required(self) -> None:
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTaxiServiceListsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test", password="test123"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self) -> None:
        Manufacturer.objects.create(name="Audi", country="Germany")
        Manufacturer.objects.create(name="Renault", country="France")
        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.all()),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_cars(self) -> None:
        manufacturer = Manufacturer.objects.create(
            name="Renault", country="France"
        )
        car = Car.objects.create(model="Logan", manufacturer=manufacturer)
        car.drivers.add(self.user)
        response = self.client.get(CAR_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]), list(Car.objects.all())
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_drivers(self) -> None:
        Driver.objects.create(license_number="ABC12345")
        response = self.client.get(DRIVER_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]), list(Driver.objects.all())
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")


class TaxiServiceCrudOperationsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test", password="test123"
        )
        self.client.force_login(self.user)

    def test_create_manufacturer(self) -> None:
        create_data = {"name": "Audi", "country": "Germany"}
        self.client.post(reverse("taxi:manufacturer-create"), data=create_data)
        manufacturer = Manufacturer.objects.get(name=create_data["name"])
        self.assertEqual(manufacturer.country, create_data["country"])

    def test_delete_car(self) -> None:
        pre_delete = Car.objects.count()
        manufacturer = Manufacturer.objects.create(
            name="Audi", country="Germany"
        )
        car = Car.objects.create(model="A5", manufacturer=manufacturer)
        self.client.post(reverse("taxi:car-delete", kwargs={"pk": car.pk}))
        after_delete = Car.objects.count()
        self.assertEqual(pre_delete, after_delete)

    def test_update_driver_license(self) -> None:
        driver = Driver.objects.create(
            username="driver", license_number="ABC12345"
        )
        new_license_number = "XYZ78910"
        url = reverse("taxi:driver-update", kwargs={"pk": driver.pk})
        self.client.post(url, {"license_number": new_license_number})
        updated_driver = Driver.objects.get(pk=driver.pk)
        self.assertEqual(updated_driver.license_number, new_license_number)


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
