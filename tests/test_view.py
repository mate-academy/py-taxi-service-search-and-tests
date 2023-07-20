from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


class PublicViewsTests(TestCase):
    def test_login_required_drivers_view(self):
        response = self.client.get(reverse("taxi:driver-list"))

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_cars_view(self):
        response = self.client.get(reverse("taxi:car-list"))

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_manufacturers_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertNotEqual(response.status_code, 200)


class PrivateViewsTests(TestCase):

    def setUp(self) -> None:
        self.paginate_by = 5
        for index in range(20):
            Driver.objects.create_user(
                username=f"test{index}",
                password=f"TestPa$${index}",
                first_name=f"John{index}",
                last_name=f"Doe{index}",
                license_number=f"JPN"
                               f"{00000 + index}"
            )
        self.client.force_login(Driver.objects.get(id=1))

        car_list = [
            ("Mazda", "CX-9"),
            ("Hyundai", "Tucson"),
            ("BMW", "X5"),
            ("Renault", "Logan"),
            ("Daewoo", "Lanos"),
            ("Rolls Royce", "Phantom")
        ]

        for brand, model in car_list:
            manufacturer = Manufacturer.objects.create(
                name=brand,
                country="TestCountry"
            )
            Car.objects.create(
                model=model,
                manufacturer=manufacturer
            )

    def test_retrieve_drivers(self):
        response = self.client.get(reverse("taxi:driver-list"))
        drivers_first_page = Driver.objects.all()[:self.paginate_by]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers_first_page)
        )

    def test_retrieve_cars(self):
        response = self.client.get(reverse("taxi:car-list"))
        cars_first_page = Car.objects.all()[:self.paginate_by]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars_first_page)
        )

    def test_retrieve_manufacturers(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        manufacturers_first_page = Manufacturer.objects.all(

        )[:self.paginate_by]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers_first_page)
        )

    def test_search_car_by_model(self):
        searched_car = "BrokenFromStart"
        response = self.client.get(reverse("taxi:car-list"), {"model": searched_car})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model__icontains=searched_car))
        )

    def test_search_manufacturer_by_name(self):
        searched_manufacturer = "Roll"
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": searched_manufacturer}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(
                name__icontains=searched_manufacturer
            ))
        )

    def test_search_driver_by_username(self):
        searched_driver = "est9"
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": searched_driver}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(Driver.objects.filter(username__icontains=searched_driver))
        )
