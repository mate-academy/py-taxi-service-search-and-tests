from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car


class PublicViewsTest(TestCase):
    def test_login_required_manufacturer_list_view(self):
        manufacturer_list_url = reverse("taxi:manufacturer-list")
        res = self.client.get(manufacturer_list_url)

        self.assertNotEquals(res.status_code, 200)

    def test_login_required_car_list_view(self):
        car_list_url = reverse("taxi:car-list")
        res = self.client.get(car_list_url)

        self.assertNotEquals(res.status_code, 200)

    def test_login_required_driver_list_view(self):
        driver_list_url = reverse("taxi:driver-list")
        res = self.client.get(driver_list_url)

        self.assertNotEquals(res.status_code, 200)


class PrivateViewsTest(TestCase):
    def setUp(self) -> None:
        cars = [
            ("Volvo", "XC60"),
            ("BMW", "M5"),
            ("Toyota", "4runner"),
            ("Mercedes", "CLS"),
            ("Nissan", "NSX100"),
            ("Ford", "Raptor"),
            ("Mazda", "Miata"),
            ("Chevrolet", "Camaro"),
            ("Dodge", "Challenger 1969"),
            ("Tesla", "ModelX"),
            ("Renault", "Megan")
        ]

        self.pagination = 5

        for car_brand, car_model in cars:
            manufacturer = Manufacturer.objects.create(
                name=car_brand
            )
            Car.objects.create(
                model=car_model,
                manufacturer=manufacturer
            )
        for i in range(12):
            Driver.objects.create_user(
                username=f"Username{i}",
                password=f"IamStrongPassword11{i}",
                first_name=f"first_name{i}",
                last_name=f"last_name{i}",
                license_number=f"ABC{10_000 + i}"
            )
        self.client.force_login(Driver.objects.get(id=1))

    def test_manufacturers_all(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.all())[:self.pagination]
        )

    def test_cars_all(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.all())[:self.pagination]
        )

    def test_drivers_all(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(Driver.objects.all())[:self.pagination]
        )

    def test_manufacturer_search(self):
        manufacturer = "Toyota"
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": manufacturer}
        )

        self.assertEqual(
            response.context["manufacturer_list"][0],
            Manufacturer.objects.get(name=manufacturer)
        )

    def test_car_search(self):
        car_model = "4runner"
        response = self.client.get(
            reverse("taxi:car-list"),
            {"car_model": car_model}
        )

        self.assertEqual(
            response.context["car_list"][0],
            Car.objects.get(model=car_model)
        )

    def test_driver_search(self):
        driver_username = "Username0"
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": driver_username}
        )

        self.assertEqual(
            response.context["driver_list"][0],
            Driver.objects.get(username=driver_username)
        )

    def test_user_assign_to_car(self):
        car = Car.objects.get(id=1)
        driver = Driver.objects.get(id=1)
        self.client.get(reverse("taxi:toggle-car-assign", kwargs={"pk": 1}))
        self.assertEqual(driver.cars.first(), car)
        self.client.get(reverse("taxi:toggle-car-assign", kwargs={"pk": 1}))
        self.assertEqual(driver.cars.count(), 0)
