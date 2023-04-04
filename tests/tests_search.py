from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURERS_URL_WITH_SEARCH = reverse("taxi:manufacturer-list") + "?name=m"
CARS_URL_WITH_SEARCH = reverse("taxi:car-list") + "?model=x"
DRIVERS_URL_WITH_SEARCH = reverse("taxi:driver-list") + "?username=v"


class SearchTests(TestCase):
    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="vasya.pupkin",
            first_name="Vasya",
            last_name="Pupkin",
            password="345ert345",
            license_number="ABC12345",
        )
        self.client.force_login(self.driver)
        Driver.objects.create(
            username="dfgsdgf",
            first_name="gfhfh",
            last_name="cvb",
            password="3ert345",
            license_number="ABC12346",
        )
        manufact1 = Manufacturer.objects.create(name="Bmw", country="Germany")
        manufact2 = Manufacturer.objects.create(name="Mazda", country="Japan")
        Car.objects.create(model="X5", manufacturer=manufact1)
        Car.objects.create(model="CX5", manufacturer=manufact2)

    def test_retrieve_manufacturer_with_search(self) -> None:
        response = self.client.get(MANUFACTURERS_URL_WITH_SEARCH)
        manufacturers = Manufacturer.objects.filter(name__icontains="m")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_car_with_search(self) -> None:
        response = self.client.get(CARS_URL_WITH_SEARCH)
        cars = Car.objects.filter(model__icontains="x")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_driver_with_search(self):
        response = self.client.get(DRIVERS_URL_WITH_SEARCH)
        drivers = Driver.objects.filter(username__icontains="v")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")
