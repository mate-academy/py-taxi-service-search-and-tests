from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_manufacturer_list_login_required(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertNotEqual(response.status_code, 200)

    def test_car_list_login_required(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertNotEqual(response.status_code, 200)

    def test_driver_list_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Voldemort", password="ban12345"
        )
        Manufacturer.objects.create(name="Mazda", country="Japan")
        Manufacturer.objects.create(name="Tesla", country="USA")

        self.client.force_login(self.user)

    def test_retrieve_manufacturers(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        manufacturers_list = Manufacturer.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers_list),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_manufacturer_search(self):
        manufacturer_filtered = Manufacturer.objects.filter(
            name__icontains="Tes"
        )
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "Tes"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturer_filtered),
        )


class PrivateCarTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Voldemort", password="ban12345"
        )
        self.manufacturer_1 = Manufacturer.objects.create(
            name="Mazda", country="Japan"
        )
        self.manufacturer_2 = Manufacturer.objects.create(
            name="Tesla", country="USA"
        )
        self.car_1 = Car.objects.create(
            model="CX-5", manufacturer=self.manufacturer_1
        )
        self.car_2 = Car.objects.create(
            model="Model S", manufacturer=self.manufacturer_2
        )
        self.client.force_login(self.user)

    def test_retrieve_cars(self):
        response = self.client.get(reverse("taxi:car-list"))
        cars_list = Car.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars_list))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_car_detail_view(self):
        response = self.client.get(
            reverse("taxi:car-detail", args=[self.car_1.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")

    def test_car_search(self):
        car_filtered = Car.objects.filter(model__icontains="Model")
        response = self.client.get(
            reverse("taxi:car-list"), {"model": "Model"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]), list(car_filtered)
        )

    def test_car_was_assigned(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car_1.id])
        self.client.get(url)
        self.assertTrue(self.car_1 in self.user.cars.all())


class PrivateDriverTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="Voldemort", password="ban12345"
        )
        self.manufacturer_1 = Manufacturer.objects.create(
            name="Mazda", country="Japan"
        )
        self.manufacturer_2 = Manufacturer.objects.create(
            name="Tesla", country="USA"
        )
        self.car_1 = Car.objects.create(
            model="CX-5", manufacturer=self.manufacturer_1
        )
        self.car_2 = Car.objects.create(
            model="Model S", manufacturer=self.manufacturer_2
        )
        self.client.force_login(self.user)

    def test_retrieve_drivers(self):
        response = self.client.get(reverse("taxi:driver-list"))
        drivers_list = get_user_model().objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]), list(drivers_list)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_driver_detail_view(self):
        response = self.client.get(
            reverse("taxi:driver-detail", args=[self.user.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")
