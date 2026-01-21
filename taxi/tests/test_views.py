from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver


class TestViews(TestCase):
    def setUp(self):
        self.auth_user = get_user_model().objects.create_superuser(
            username="admin",
            first_name="Admin",
            last_name="Admin",
            license_number="ABC98765",
        )
        self.client.force_login(self.auth_user)

    def test_manufacturer_list_view(self):
        Manufacturer.objects.create(
            name="BWM",
            country="Germany",
        )
        Manufacturer.objects.create(
            name="Skoda",
            country="Czech Republic",
        )
        manufacturers = Manufacturer.objects.all()
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(
            list(response.context["manufacturer_list"]), list(manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_manufacturer_by_name(self):
        manufacturer1 = Manufacturer.objects.create(
            name="BWM",
            country="Germany",
        )
        manufacturer2 = Manufacturer.objects.create(
            name="Skodaw",
            country="Czech Republic",
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "m"}
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]), [manufacturer1]
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "a"}
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]), [manufacturer2]
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "e"}
        )
        self.assertEqual(list(response.context["manufacturer_list"]), [])

        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.all()),
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "w"}
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            [manufacturer1, manufacturer2],
        )

    def test_search_driver_by_username(self):
        admin1 = get_user_model().objects.create_superuser(
            username="moving",
            first_name="Admin",
            last_name="Admin",
            license_number="CDE876234",
        )
        admin2 = get_user_model().objects.create_superuser(
            username="stag",
            first_name="Admin",
            last_name="Admin",
            license_number="BIE00238",
        )

        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "v"}
        )
        self.assertEqual(list(response.context["driver_list"]), [admin1])

        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "s"}
        )
        self.assertEqual(list(response.context["driver_list"]), [admin2])

        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "z"}
        )
        self.assertEqual(list(response.context["driver_list"]), [])

        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(
            list(response.context["driver_list"]), list(Driver.objects.all())
        )

        response = self.client.get(
            reverse("taxi:driver-list"), {"username": "g"}
        )
        self.assertEqual(
            list(response.context["driver_list"]), [admin1, admin2]
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_search_car_by_model(self):
        manufacturer = Manufacturer.objects.create(
            name="BWM",
            country="Germany",
        )
        car1 = Car.objects.create(
            manufacturer=manufacturer,
            model="E93",
        )
        car2 = Car.objects.create(
            manufacturer=manufacturer,
            model="M3",
        )

        response = self.client.get(reverse("taxi:car-list"), {"model": "9"})
        self.assertEqual(list(response.context["car_list"]), [car1])

        response = self.client.get(reverse("taxi:car-list"), {"model": "m"})
        self.assertEqual(list(response.context["car_list"]), [car2])

        response = self.client.get(reverse("taxi:car-list"), {"model": "0"})
        self.assertEqual(list(response.context["car_list"]), [])

        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(
            list(response.context["car_list"]), list(Car.objects.all())
        )

        response = self.client.get(reverse("taxi:car-list"), {"model": "3"})
        self.assertEqual(list(response.context["car_list"]), [car1, car2])
        self.assertTemplateUsed(response, "taxi/car_list.html")
