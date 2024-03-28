from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class LoginRequiredCarViewTest(TestCase):
    def test_login_required_manufacturer_list(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 302)

    def test_login_required_manufacturer_create(self):
        response = self.client.get(reverse("taxi:car-create"))
        self.assertEqual(response.status_code, 302)

    def test_login_required_car_detail(self):
        response = self.client.get(reverse(
            "taxi:car-detail",
            kwargs={"pk": 1}
        ))
        self.assertEqual(response.status_code, 302)

    def test_login_required_manufacturer_update(self):
        response = self.client.get(reverse(
            "taxi:car-update",
            kwargs={"pk": 1}
        ))
        self.assertEqual(response.status_code, 302)

    def test_login_required_manufacturer_delete(self):
        response = self.client.get(reverse(
            "taxi:car-delete",
            kwargs={"pk": 1}
        ))
        self.assertEqual(response.status_code, 302)

    def test_login_required_driver_detail(self):
        response = self.client.get(reverse(
            "taxi:toggle-car-assign",
            kwargs={"pk": 1}
        ))
        self.assertEqual(response.status_code, 302)


class CarViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_cars = 4
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        for car_id in range(number_of_cars):
            Car.objects.create(
                model=f"Test{car_id}",
                manufacturer=manufacturer
            )

    def setUp(self):
        self.driver = Driver.objects.create(
            username="Test1",
            password="12345",
            license_number="ABC12345"
        )
        self.client.force_login(self.driver)
        self.car = Car.objects.get(id=1)

    def test_list_cars(self):
        response = self.client.get(reverse("taxi:car-list"))
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(cars))

    def test_filter_list_cars(self):
        response = self.client.get(f"{reverse('taxi:car-list')}?model=1")
        self.assertEqual(len(response.context["car_list"]), 1)

    def test_pagination_list_drivers(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW2.0",
            country="Germany"
        )
        for car_id in range(9):
            Car.objects.create(
                model=f"Test2{car_id}",
                manufacturer=manufacturer
            )
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["car_list"]), 5)

        response = self.client.get(
            f"{reverse("taxi:car-list")}?model=2&page=2"
        )
        self.assertEqual(response.context["paginator"].num_pages, 2)

    def test_car_detail_correct_data(self):
        response = self.client.get(reverse(
            "taxi:car-detail",
            kwargs={"pk": self.car.id}
        ))
        self.assertContains(response, self.car.model)
        self.assertContains(response, self.car.manufacturer.name)
        self.assertContains(response, self.car.manufacturer.country)

    def test_car_create_get(self):
        response = self.client.get(reverse("taxi:car-create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Model")
        self.assertContains(response, "Manufacturer")

    def test_car_create_post(self):
        driver = Driver.objects.create(
            username="Username",
            password="12345",
            license_number="ABC12346"
        )
        data = {
            "model": "3 Series",
            "manufacturer": self.car.manufacturer.id,
            "drivers": [driver.id]
        }
        self.client.post(reverse("taxi:car-create"), data=data)
        new_car = Car.objects.get(model=data["model"])
        self.assertEqual(new_car.model, data["model"])
        self.assertEqual(new_car.manufacturer.id, data["manufacturer"])

    def test_car_update_get(self):
        response = self.client.get(reverse(
            "taxi:car-update",
            kwargs={"pk": self.car.id}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.model)
        self.assertContains(response, self.car.manufacturer.name)

    def test_car_update_post(self):
        driver = Driver.objects.create(
            username="Username2",
            password="12345",
            license_number="ABC12346"
        )
        data = {
            "model": "33 Series",
            "manufacturer": self.car.manufacturer.id,
            "drivers": [driver.id]
        }
        self.client.post(reverse(
            "taxi:car-update",
            kwargs={"pk": self.car.id}), data=data
        )
        new_car = Car.objects.get(model=data["model"])
        self.assertEqual(list(new_car.drivers.all()), [driver])

    def test_car_delete_get(self):
        response = self.client.get(reverse(
            "taxi:car-delete",
            kwargs={"pk": self.car.id}
        ))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delete car?")

    def test_car_delete_post(self):
        self.client.post(reverse(
            "taxi:car-delete",
            kwargs={"pk": self.car.id}
        ))
        ls = Car.objects.filter(model=self.car.model)
        self.assertEqual(len(ls), 0)

    def test_car_toggle(self):
        self.client.post(reverse(
            "taxi:toggle-car-assign",
            kwargs={"pk": self.car.id}
        ))
        self.assertTrue(self.car in self.driver.cars.all())
        self.client.post(reverse(
            "taxi:toggle-car-assign",
            kwargs={"pk": self.car.id}
        ))
        self.assertTrue(self.car not in self.driver.cars.all())
