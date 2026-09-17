from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver


class ViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manufacturer = Manufacturer.objects.create(name="Tesla",
                                                       country="USA")
        cls.driver = Driver.objects.create_user(username="John123",
                                                password="1234")
        cls.car = Car.objects.create(model="Model S",
                                     manufacturer=cls.manufacturer)
        cls.car.drivers.add(cls.driver)

        cls.url_index = reverse("taxi:index")

        cls.url_manufacturer_list = reverse("taxi:manufacturer-list")
        cls.url_manufacturer_create = reverse("taxi:manufacturer-create")
        cls.url_manufacturer_update = reverse(
            "taxi:manufacturer-update",
            kwargs={"pk": cls.manufacturer.pk}
        )
        cls.url_manufacturer_delete = reverse(
            "taxi:manufacturer-delete",
            kwargs={"pk": cls.manufacturer.pk}
        )

        cls.url_car_list = reverse("taxi:car-list")
        cls.url_car_detail = reverse("taxi:car-detail",
                                     kwargs={"pk": cls.car.pk})
        cls.url_car_create = reverse("taxi:car-create")
        cls.url_car_update = reverse("taxi:car-update",
                                     kwargs={"pk": cls.car.pk})
        cls.url_car_delete = reverse("taxi:car-delete",
                                     kwargs={"pk": cls.car.pk})

        cls.url_driver_list = reverse("taxi:driver-list")
        cls.url_driver_detail = reverse(
            "taxi:driver-detail", kwargs={"pk": cls.driver.pk}
        )
        cls.url_driver_create = reverse("taxi:driver-create")
        cls.url_driver_update = reverse(
            "taxi:driver-update", kwargs={"pk": cls.driver.pk}
        )
        cls.url_driver_delete = reverse(
            "taxi:driver-delete", kwargs={"pk": cls.driver.pk}
        )

    def test_accessible_by_anonymous_user(self):
        data = [
            self.url_index,
            self.url_manufacturer_list,
            self.url_manufacturer_create,
            self.url_manufacturer_update,
            self.url_manufacturer_delete,
            self.url_car_list,
            self.url_car_detail,
            self.url_car_create,
            self.url_car_update,
            self.url_car_delete,
            self.url_driver_list,
            self.url_driver_detail,
            self.url_driver_create,
            self.url_driver_update,
            self.url_driver_delete,
        ]

        for url in data:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)

    def test_index_view_context_and_session(self):
        self.client.login(username="John123", password="1234")
        response = self.client.get(self.url_index)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_drivers"], 1)
        self.assertEqual(response.context["num_manufacturers"], 1)
        self.assertEqual(response.context["num_visits"], 1)
        response2 = self.client.get(self.url_index)
        self.assertEqual(response2.context["num_visits"], 2)

    def test_driver_list_view_get_queryset_and_get_context_data(self):
        self.client.login(username="John123", password="1234")
        Driver.objects.create_user(
            username="Alex123", license_number="ABC54321", password="1234"
        )
        response = self.client.get(self.url_driver_list,
                                   {"username": "John"})

        drivers_in_response = response.context["driver_list"]

        self.assertEqual(len(drivers_in_response), 1)
        self.assertEqual(drivers_in_response[0], self.driver)

        self.assertIn("search_form", response.context)
        self.assertEqual(response.context["search_form"].initial["username"],
                         "John")

    def test_toggle_assign_to_car(self):
        self.client.login(username="John123", password="1234")
        url = reverse("taxi:toggle-car-assign",
                      kwargs={"pk": self.car.id})
        expected_redirect_url = reverse("taxi:car-detail",
                                        kwargs={"pk": self.car.id})
        self.assertIn(self.car, self.driver.cars.all())
        response = self.client.get(url)
        self.assertRedirects(response, expected_redirect_url)
        self.assertNotIn(self.car, self.driver.cars.all())

        response2 = self.client.get(url)
        self.assertRedirects(response2, expected_redirect_url)
        self.assertIn(self.car, self.driver.cars.all())

    def test_car_view_get_queryset_and_get_context_data(self):
        self.client.login(username="John123", password="1234")
        model_x = Car.objects.create(
            model="Model X",
            manufacturer=self.manufacturer,
        )
        model_x.drivers.add(self.driver)

        response = self.client.get(self.url_car_list, {"model": "S"})

        cars_in_response = response.context["car_list"]

        self.assertEqual(len(cars_in_response), 1)
        self.assertEqual(cars_in_response[0], self.car)

        self.assertIn("search_form", response.context)
        self.assertEqual(response.context["search_form"].initial["model"],
                         "S")

    def test_manufacturer_view_get_queryset_and_get_context_data(self):
        self.client.login(username="John123", password="1234")
        Manufacturer.objects.create(
            name="Mercedes",
            country="Ukraine",
        )

        response = self.client.get(self.url_manufacturer_list,
                                   {"name": "Tesla"})

        manufacturer_in_response = response.context["manufacturer_list"]

        self.assertEqual(len(manufacturer_in_response), 1)
        self.assertEqual(manufacturer_in_response[0], self.manufacturer)

        self.assertIn("search_form", response.context)
        self.assertEqual(response.context["search_form"].initial["name"],
                         "Tesla")
