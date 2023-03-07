from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


class SearchTests(TestCase):
    NUM_OBJECTS = 5

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="new_user",
            license_number="ADM56984"
        )
        self.client.force_login(self.user)

    def test_search_manufacturer_by_name(self):

        for manufacturer_num in range(self.NUM_OBJECTS):
            Manufacturer.objects.create(
                name=f"BMW{manufacturer_num}",
                country="Germany"
            )
        Manufacturer.objects.create(name="Mercedes-Benz", country="Germany")
        Manufacturer.objects.create(name="Toyota", country="Japan")

        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=BMW"
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__icontains="BMW")),
        )

    def test_search_cars_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="Toyota",
            country="Japan"
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Nissan",
            country="Japan"
        )
        for car_num in range(self.NUM_OBJECTS):
            Car.objects.create(
                model=f"Yaris{car_num}",
                manufacturer=manufacturer
            )
        Car.objects.create(model="Note", manufacturer=manufacturer2)

        response = self.client.get(reverse("taxi:car-list") + "?name=Yaris")
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model__icontains="Yaris")),
        )

    def test_search_drivers_by_username(self):
        for user_num in range(self.NUM_OBJECTS):
            get_user_model().objects.create_user(
                username=f"test{user_num}",
                license_number=f"QWE1234{user_num}"
            )

        response = self.client.get(
            reverse("taxi:driver-list") + "?username=test"
        )
        self.assertEqual(
            list(response.context["driver_list"]),
            list(Driver.objects.filter(username__icontains="test")),
        )
