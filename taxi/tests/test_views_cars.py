from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver

CAR_LIST_URL = reverse("taxi:car-list")


class CarPublicTest(TestCase):

    def test_car_list_logout(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertNotEquals(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=%2Fcars%2F")

    def test_car_detail(self):
        manufacturer = Manufacturer.objects.create(
            name="test1",
            country="TestCountry1"
        )
        car = Car.objects.create(model="test1", manufacturer=manufacturer)

        url = reverse("taxi:car-detail", kwargs={"pk": car.id})
        response = self.client.get(url)

        self.assertNotEquals(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=%2Fcars%2F1%2F")


class CarPrivateTest(TestCase):

    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test_driver",
            first_name="test_fn",
            last_name="test_ln",
            password="test_pass123",
            license_number="TES12345"
        )

        self.driver2 = get_user_model().objects.create_user(
            username="test_driver2",
            first_name="test_fn2",
            last_name="test_ln2",
            password="test_pass12322",
            license_number="TES1234522"
        )

        self.client.force_login(self.driver)

        self.manufacturer = Manufacturer.objects.create(
            name="test1",
            country="TestCountry1"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="test2",
            country="TestCountry2"
        )

        self.instance = Car.objects.create(
            model="testmodel",
            manufacturer=self.manufacturer
        )
        self.instance.drivers.add(self.driver)

        self.driver3 = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )
        self.client.login(
            username="testuser",
            password="testpassword"
        )

    def test_car_create(self):
        url = reverse("taxi:car-create")
        data = {
            "model": "testmodel",
            "manufacturer": self.manufacturer.id,
            "drivers": [self.driver.id]
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)

        car = Car.objects.get(id=1)

        self.assertEqual(car.model, "testmodel")
        self.assertEqual(car.manufacturer.name, "test1")
        self.assertEquals(list(car.drivers.all()), [self.driver])

    def test_car_update(self):
        url = reverse("taxi:car-update", kwargs={"pk": self.instance.id})
        data = {
            "model": "testmodel2",
            "manufacturer": self.manufacturer2.id,
            "drivers": [self.driver2.id]
        }

        response = self.client.post(url, data)

        self.instance.refresh_from_db()

        self.assertEquals(response.status_code, 302)
        self.assertEquals(self.instance.model, "testmodel2")
        self.assertEquals(self.instance.manufacturer, self.manufacturer2)
        self.assertEquals(list(self.instance.drivers.all()), [self.driver2])

    def test_car_delete(self):
        url = reverse("taxi:car-delete", kwargs={"pk": self.instance.id})

        response = self.client.post(url)

        self.assertEquals(response.status_code, 302)
        self.assertFalse(Car.objects.filter(id=self.instance.id).exists())
        self.assertRedirects(response, reverse("taxi:car-list"))

    def test_car_assign(self):
        self.assertEqual(
            Driver.objects.get(
                id=self.driver3.id
            ).cars.count(),
            0
        )

        response = self.client.get(
            reverse(
                "taxi:toggle-car-assign",
                args=[self.instance.pk]
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Driver.objects.get(
                id=self.driver3.id
            ).cars.count(),
            1
        )
        self.assertEqual(
            Driver.objects.get(
                id=self.driver3.id
            ).cars.first(),
            self.instance
        )

        response = self.client.get(
            reverse(
                "taxi:toggle-car-assign",
                args=[self.instance.pk]
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Driver.objects.get(
                id=self.driver3.id
            ).cars.count(), 0)
