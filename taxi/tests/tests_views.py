from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicViewsTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required_for_list_views(self):
        urls = [
            reverse("taxi:manufacturer-list"),
            reverse("taxi:car-list"),
            reverse("taxi:driver-list"),
        ]
        for url in urls:
            res = self.client.get(url)
            self.assertNotEqual(res.status_code, 200)
            self.assertIn(res.status_code, [302, 301])


class PrivateListViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test-user",
            password="1qazcde3",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

        self.manuf1 = Manufacturer.objects.create(name="Audi", country="DE")
        self.manuf2 = Manufacturer.objects.create(name="BMW", country="DE")

        self.car1 = Car.objects.create(model="A4", manufacturer=self.manuf1)
        self.car2 = Car.objects.create(model="M3", manufacturer=self.manuf2)

    def test_manufacturer_list_view(self):
        res = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(res.status_code, 200)
        expected = list(Manufacturer.objects.order_by("name"))
        self.assertEqual(list(res.context["manufacturer_list"]), expected)
        self.assertTemplateUsed(
            res,
            "taxi/manufacturer_list.html"
        )

    def test_car_list_view(self):
        res = self.client.get(reverse("taxi:car-list"))

        self.assertEqual(res.status_code, 200)
        expected = list(Car.objects.all())
        self.assertEqual(list(res.context["car_list"]), expected)
        self.assertTemplateUsed(res, "taxi/car_list.html")

    def test_driver_list_view(self):
        res = self.client.get(reverse("taxi:driver-list"))

        self.assertEqual(res.status_code, 200)
        expected = list(get_user_model().objects.all())
        self.assertEqual(list(res.context["driver_list"]), expected)
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_search_in_manufacturer_list(self):
        url = reverse("taxi:manufacturer-list")
        res = self.client.get(url + "?search_term=Audi")

        manufacturers = Manufacturer.objects.filter(name__icontains="Audi")
        self.assertEqual(list(res.context["manufacturer_list"]),
                         list(manufacturers))

    def test_search_in_car_list(self):
        url = reverse("taxi:car-list")
        res = self.client.get(url + "?search_term=A4")

        cars = Car.objects.filter(model__icontains="A4")
        self.assertEqual(list(res.context["car_list"]), list(cars))

    def test_search_in_driver_list(self):
        url = reverse("taxi:driver-list")
        res = self.client.get(url + "?search_term=test")

        drivers = get_user_model().objects.filter(username__icontains="test")
        self.assertEqual(list(res.context["driver_list"]), list(drivers))

    def test_search_form_in_context(self):
        res = self.client.get(reverse("taxi:car-list"))
        self.assertIn("search_form", res.context)


class ToggleAssignToCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="d1",
            password="testpass",
            license_number="ABC12345",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="VW",
            country="DE",
        )
        self.car = Car.objects.create(
            model="Passat",
            manufacturer=self.manufacturer,
        )
        self.client = Client()
        self.client.force_login(self.user)

    def test_assign_car(self):
        url = reverse("taxi:toggle-car-assign", args=[self.car.id])

        self.client.get(url)

        self.assertIn(self.car, self.user.cars.all())

    def test_unassign_car(self):
        self.user.cars.add(self.car)
        url = reverse("taxi:toggle-car-assign", args=[self.car.id])

        self.client.get(url)

        self.assertNotIn(self.car, self.user.cars.all())
