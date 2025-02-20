from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ModelsTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Jeep",
            country="USA"
        )
        self.assertEqual(
            str(manufacturer),
            f"{manufacturer.name} {manufacturer.country}"
        )

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="Jeep",
            country="USA"
        )
        car = Car.objects.create(
            model="JeepTestModel",
            manufacturer=manufacturer
        )
        self.assertEqual(str(car), f"{car.model}")

    def test_driver_str(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            first_name="test_first",
            last_name="test_last"
        )
        self.assertEqual(
            str(driver),
            f"{driver.username} ({driver.first_name} {driver.last_name})"
        )

    def test_driver_absolute_url(self):
        driver = get_user_model().objects.create_user(
            username="test",
            password="test1234",
            first_name="test_first",
            last_name="test_last"
        )
        self.assertEqual(
            driver.get_absolute_url(),
            reverse("taxi:driver-detail",
                    kwargs={"pk": driver.pk})
        )
class PrivateCarListTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test1234"
        )
        self.client.force_login(self.user)

        ferrari = Manufacturer.objects.create(name="Ferrari", country="Italy")
        lambo = Manufacturer.objects.create(name="Lambo", country="Italy")
        ford = Manufacturer.objects.create(name="Ford", country="USA")

        Car.objects.create(model="Ferrari Aguero", manufacturer=ferrari)
        Car.objects.create(model="Lambo Viesta", manufacturer=lambo)
        Car.objects.create(model="Ford Fusion", manufacturer=ford)
        Car.objects.create(model="Ford Fiesta", manufacturer=ford)

    def test_get_car_list(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

    def test_search_car_by_model(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=Ford")

        self.assertEqual(response.status_code, 200)

        actual = response.context.get("car_list")
        expected = Car.objects.filter(model__icontains="Ford")

        self.assertEqual(list(actual), list(expected))

        response = self.client.get(reverse("taxi:car-list") + "?model=Viesta")
        actual = response.context.get("car_list")
        expected = Car.objects.filter(model__icontains="Viesta")

        self.assertEqual(list(actual), list(expected))

    def test_empty_field_search(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=")

        self.assertEqual(response.status_code, 200)

        actual = response.context.get("car_list")
        expected = Car.objects.all()

        self.assertEqual(list(actual), list(expected))
