from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer


DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")
MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")


class PublicDriverTests(TestCase):

    def test_login_required(self) -> None:
        response = self.client.get(DRIVER_LIST_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            license_number="TST12345",
        )
        self.client.force_login(self.user)

    def test_retrieve_driver_list(self) -> None:
        Driver.objects.create_user(username="testuser2")
        response = self.client.get(DRIVER_LIST_URL)
        drivers = Driver.objects.all()

        self.assertEqual(
            tuple(response.context["driver_list"]),
            tuple(drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_filtered_driver_list(self) -> None:
        Driver.objects.bulk_create(
            [
                Driver(username="testuser22", license_number="TST12344"),
                Driver(username="testuser3", license_number="TST12346"),
                Driver(username="testuser23", license_number="TST12341"),
            ]
        )
        response = self.client.get(
            DRIVER_LIST_URL,
            query_params={"username": "2"}
        )
        filtered_drivers = Driver.objects.filter(username__icontains="2")

        self.assertEqual(
            tuple(response.context["driver_list"]),
            tuple(filtered_drivers)
        )


class PrivateCarTests(TestCase):

    def setUp(self) -> None:
        self.manufacturer = Manufacturer.objects.create(
            name="Test manufacturer",
            country="Test country"
        )
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test12345",
        )

        self.client.force_login(self.user)

    def test_retrieve_car_list(self) -> None:

        Car.objects.create(
            model="Test model1",
            manufacturer=self.manufacturer,
        )
        Car.objects.create(
            model="Test model2",
            manufacturer=self.manufacturer
        )
        response = self.client.get(CAR_LIST_URL)
        cars = Car.objects.all()

        self.assertEqual(
            tuple(response.context["car_list"]),
            tuple(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_filtered_car_list(self) -> None:
        model = "model"
        Car.objects.bulk_create(
            [
                Car(model="Test model", manufacturer=self.manufacturer),
                Car(model="Test car", manufacturer=self.manufacturer),
                Car(model="Test model car", manufacturer=self.manufacturer)
            ]
        )
        response = self.client.get(
            CAR_LIST_URL,
            query_params={"model": model}
        )

        self.assertEqual(
            tuple(response.context["car_list"]),
            tuple(Car.objects.filter(model__icontains=model))
        )


class PrivateManufacturerTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test1234",
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturer_list(self) -> None:
        country = "Test country"
        Manufacturer.objects.bulk_create(
            [
                Manufacturer(name="Test manufacturer1", country=country),
                Manufacturer(name="Test manufacturer2", country=country)
            ]
        )
        response = self.client.get(MANUFACTURER_LIST_URL)
        self.assertEqual(
            tuple(response.context["manufacturer_list"]),
            tuple(Manufacturer.objects.all())
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_filtered_manufacturer_list(self) -> None:
        country = "Test country"
        Manufacturer.objects.bulk_create(
            [
                Manufacturer(name="Test manufacturer1", country=country),
                Manufacturer(name="Test manufacturer12", country=country),
                Manufacturer(name="Test manufacturer", country=country)
            ]
        )
        response = self.client.get(
            MANUFACTURER_LIST_URL,
            query_params={"name": "1"}
        )
        self.assertEqual(
            tuple(response.context["manufacturer_list"]),
            tuple(Manufacturer.objects.filter(name__icontains="1"))
        )
