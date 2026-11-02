from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Car, Manufacturer


class PublicUserTests(TestCase):
    def test_search_without_login(self):
        url = reverse("taxi:car-list")
        res = self.client.get(url)

        self.assertNotEqual(res.status_code, 200)


class ViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="qqqq",
            password="QCold999",
            license_number="TCP00999"
        )
        self.client.force_login(user=self.user)

    def test_manufacturer_search(self):
        toyota = Manufacturer.objects.create(name="Toyota")
        Manufacturer.objects.create(name="BMW")
        ford = Manufacturer.objects.create(name="Ford")

        url = reverse("taxi:manufacturer-list")
        response = self.client.get(url, {"name": "o"})
        self.assertCountEqual(
            response.context["manufacturer_list"],
            [toyota, ford],
        )

    def test_car_search(self):
        manuf = Manufacturer.objects.create(
            name="Toyota"
        )
        camry = Car.objects.create(model="Camry", manufacturer=manuf)
        corolla = Car.objects.create(model="Corolla", manufacturer=manuf)
        Car.objects.create(model="Hilux", manufacturer=manuf)

        url = reverse("taxi:car-list")
        response = self.client.get(url, {"model": "c"})
        self.assertCountEqual(
            response.context["car_list"],
            [camry, corolla],
        )

    def test_driver_search(self):
        get_user_model().objects.create_user(
            username="Dave",
            password="David1234",
            license_number="TCP33999"
        )

        alice = get_user_model().objects.create_user(
            username="Alice",
            password="Alice1234",
            license_number="TCP66999"
        )

        alex = get_user_model().objects.create_user(
            username="Alex",
            password="Alex1234",
            license_number="TCP99999"
        )

        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"username": "l"})
        self.assertCountEqual(
            response.context["driver_list"],
            [alice, alex],
        )

    def test_search_login_user_home_page(self):
        url = reverse("taxi:index")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_new_driver_to_car(self):
        driver = get_user_model().objects.create_user(
            username="Dave",
            password="David1234",
            license_number="TCP33999"
        )
        manuf = Manufacturer.objects.create(
            name="Toyota"
        )
        car = Car.objects.create(
            model="Camry",
            manufacturer=manuf,
        )
        car.drivers.add(driver)

        url = reverse("taxi:toggle-car-assign", kwargs={"pk": car.pk})
        self.client.get(url)
        self.assertTrue(
            car.drivers.filter(pk=self.user.pk).exists()
        )
        self.client.get(url)
        self.assertFalse(
            car.drivers.filter(pk=self.user.pk).exists()
        )
