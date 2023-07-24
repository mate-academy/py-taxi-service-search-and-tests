from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car

DRIVERS_URL = reverse("taxi:driver-list")
CARS_URL = reverse("taxi:car-list")
MANUFACTURERS_URL = reverse("taxi:manufacturer-list")


class PublicViewsTests(TestCase):
    def test_login_required_drivers_view(self):
        response = self.client.get(DRIVERS_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_cars_view(self):
        response = self.client.get(CARS_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_manufacturers_view(self):
        response = self.client.get(MANUFACTURERS_URL)

        self.assertNotEqual(response.status_code, 200)


class PrivateViewsTests(TestCase):

    def setUp(self) -> None:
        self.paginate_by = 5
        for index in range(20):
            Driver.objects.create_user(
                username=f"Test{index}",
                password=f"TestPassword12{index}",
                first_name=f"Robot{index}",
                last_name=f"Smith{index}",
                license_number=f"AAA"
                               f"{00000 + index}"
            )
        self.client.force_login(Driver.objects.get(id=1))

        car_list = [
            ("VAZ", "Broken1"),
            ("Tesla", "Model Y"),
            ("BMW", "X5"),
            ("Riot Cars", "BrokenFromStartV1"),
            ("Renault", "Logan"),
            ("Wolkswagen", "Passat"),
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
        response = self.client.get(DRIVERS_URL)
        drivers_first_page = Driver.objects.all()[:self.paginate_by]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(drivers_first_page)
        )

    def test_retrieve_cars(self):
        response = self.client.get(CARS_URL)
        cars_first_page = Car.objects.all()[:self.paginate_by]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(cars_first_page)
        )

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURERS_URL)
        manufacturers_first_page = Manufacturer.objects.all(

        )[:self.paginate_by]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers_first_page)
        )

    def test_search_car_by_model(self):
        searched_car = "BrokenFromStart"
        response = self.client.get(CARS_URL, {"model": searched_car})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model__icontains=searched_car))
        )

    def test_search_manufacturer_by_name(self):
        searched_manufacturer = "Roll"
        response = self.client.get(MANUFACTURERS_URL,
                                   {"name": searched_manufacturer})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(
                name__icontains=searched_manufacturer
            ))
        )

    def test_search_driver_by_username(self):
        searched_driver = "est9"
        response = self.client.get(DRIVERS_URL,
                                   {"username": searched_driver})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(Driver.objects.filter(username__icontains=searched_driver))
        )

    def test_assign_driver_to_car(self):
        driver = Driver.objects.create(
            username=f"Kevin123",
            password=f"TestPassword12",
            email="example@example.com",
            first_name=f"Robot",
            last_name=f"Smith",
            license_number="ABC12345"
        )
        car = Car.objects.create(model="Lamder",
                                 manufacturer=Manufacturer.objects.create(
                                     name="Test",
                                     country="Test"
                                 ))
        car.drivers.add(driver)
        car.save()
        url = reverse("taxi:toggle-car-assign", args=[car.pk])

        self.assertIn(car, driver.cars.all())

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

        self.assertIn(car, driver.cars.all())
