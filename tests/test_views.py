from django.urls import reverse

from tests.test_setup import TestSetUp

MANUFACTURER_LIST_URL = reverse("taxi:manufacturer-list")
DRIVER_LIST_URL = reverse("taxi:driver-list")
CAR_LIST_URL = reverse("taxi:car-list")


class PublicTests(TestSetUp):
    def test_login_required_manufacturer_list(self):
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_driver_list(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_driver_detail(self):
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk})
        )

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_car_list(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertNotEqual(response.status_code, 200)

    def test_login_required_car_detail(self):
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": self.car.pk})
        )

        self.assertNotEqual(response.status_code, 200)


class PrivateTests(TestSetUp):
    def setUp(self):
        super().setUp()
        self.client.force_login(self.driver)

    def test_retrieve_manufacturers(self):
        response = self.client.get(MANUFACTURER_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(self.manufacturers)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_retrieve_drivers(self):
        response = self.client.get(DRIVER_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(self.drivers)
        )
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_cars(self):
        response = self.client.get(CAR_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["car_list"]), list(self.cars))
        self.assertTemplateUsed(response, "taxi/car_list.html")
