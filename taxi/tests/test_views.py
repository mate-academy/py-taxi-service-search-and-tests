from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")


class ListViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test", password="P@ssword23", license_number="ABC12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test", country="Ukraine"
        )
        self.car = Car.objects.create(
            model="test", manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.user)
        self.client.force_login(self.user)

    def test_manufacturers_searching_feature(self) -> None:
        Manufacturer.objects.create(name="another_test", country="Ukraine")

        form_data = {"name": "another"}
        response = self.client.get(MANUFACTURER_URL, data=form_data)
        queryset = Manufacturer.objects.filter(name__icontains="another")
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(queryset)
        )

    def test_cars_searching_feature(self) -> None:
        car = Car.objects.create(
            model="one_more_test",
            manufacturer=self.manufacturer,
        )
        car.drivers.add(self.user)

        form_data = {"model": "more"}
        response = self.client.get(CAR_URL, data=form_data)
        queryset = Car.objects.filter(model__icontains="more")
        self.assertEqual(list(response.context["car_list"]), list(queryset))

    def test_drivers_searching_feature(self) -> None:
        get_user_model().objects.create_user(
            username="last_test",
            password="P@ssword23",
            license_number="AAA12345",
        )

        form_data = {"username": "t_"}
        response = self.client.get(DRIVER_URL, data=form_data)
        queryset = get_user_model().objects.filter(username__icontains="t_")
        self.assertEqual(list(response.context["driver_list"]), list(queryset))


class UpdateViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test", password="P@ssword23", license_number="ABC12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test", country="Ukraine"
        )
        self.car = Car.objects.create(
            model="test", manufacturer=self.manufacturer
        )
        self.car.drivers.add(self.user)
        self.client.force_login(self.user)

    def test_toggle_car_assign(self):
        response = self.client.get(reverse('taxi:toggle-car-assign', args=[self.car.pk]))
        self.assertRedirects(response, reverse('taxi:car-detail', args=[self.car.pk]))
        self.assertFalse(self.car in self.user.cars.all())
        another_user = get_user_model().objects.create_user(
            username="another_test", password="P@ssword23", license_number="ABC12312"
        )
        self.client.force_login(another_user)
        response = self.client.get(reverse('taxi:toggle-car-assign', args=[self.car.pk]))
        self.assertRedirects(response, reverse('taxi:car-detail', args=[self.car.pk]))
        self.assertTrue(self.car in another_user.cars.all())
