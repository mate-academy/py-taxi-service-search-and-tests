from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car, Driver

MANUFACTURER_VIEW_LIST_URL = reverse("taxi:manufacturer-list")
MANUFACTURER_CREATE_VIEW_URL = reverse("taxi:manufacturer-create")

CAR_VIEW_LIST_URL = reverse("taxi:car-list")
CAR_CREATE_VIEW_URL = reverse("taxi:car-create")

DRIVER_VIEW_LIST_URL = reverse("taxi:driver-list")
DRIVER_CREATE_VIEW_URL = reverse("taxi:driver-create")


class PublicManufacturerViewTest(TestCase, Manufacturer):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="BMW",
                                                        country="Germany")
        self.driver = Driver.objects.create(username="Alex",
                                            password="<PASSWORD>")
        self.car = Car.objects.create(model="5",
                                      manufacturer=self.manufacturer)

    def test_manufacturer_view_list(self):
        res = self.client.get(MANUFACTURER_VIEW_LIST_URL)
        self.assertNotEquals(res.status_code, 200)

    def test_manufacturer_update(self):
        manufacturer_update_view_url = reverse("taxi:manufacturer-update",
                                               args=[self.manufacturer.id])
        res = self.client.get(manufacturer_update_view_url)
        self.assertNotEquals(res.status_code, 200)

    def test_manufacturer_create(self):
        res = self.client.get(MANUFACTURER_CREATE_VIEW_URL)
        self.assertNotEquals(res.status_code, 200)

    def test_manufacturer_delete(self):
        manufacturer_delete_view_url = reverse("taxi:manufacturer-delete",
                                               args=[self.manufacturer.id])
        res = self.client.get(manufacturer_delete_view_url)
        self.assertNotEquals(res.status_code, 200)

    def test_car_list(self):
        res = self.client.get(CAR_VIEW_LIST_URL)
        self.assertNotEquals(res.status_code, 200)

    def test_car_detail(self):
        car_detail_view_url = reverse("taxi:car-detail",
                                      args=[self.car.id])
        res = self.client.get(car_detail_view_url)
        self.assertNotEquals(res.status_code, 200)

    def test_car_create(self):
        res = self.client.get(CAR_CREATE_VIEW_URL)
        self.assertNotEquals(res.status_code, 200)

    def test_car_update(self):
        car_update_view_url = reverse("taxi:car-update",
                                      args=[self.car.id])
        res = self.client.get(car_update_view_url)
        self.assertNotEquals(res.status_code, 200)

    def test_car_delete(self):
        car_delete_view_url = reverse("taxi:car-delete",
                                      args=[self.car.id])
        res = self.client.get(car_delete_view_url)
        self.assertNotEquals(res.status_code, 200)

    def test_driver_list(self):
        res = self.client.get(DRIVER_VIEW_LIST_URL)
        self.assertNotEquals(res.status_code, 200)

    def test_driver_create(self):
        res = self.client.get(DRIVER_CREATE_VIEW_URL)
        self.assertNotEquals(res.status_code, 200)

    def test_driver_detail(self):
        driver_detail_view_url = reverse("taxi:driver-detail",
                                         args=[self.driver.id])
        res = self.client.get(driver_detail_view_url)
        self.assertNotEquals(res.status_code, 200)

    def test_driver_delete(self):
        driver_delete_view_url = reverse("taxi:driver-delete",
                                         args=[self.driver.id])
        res = self.client.get(driver_delete_view_url)
        self.assertNotEquals(res.status_code, 200)

    def test_driver_update(self):
        driver_update_url = reverse("taxi:driver-update",
                                    args=[self.driver.id])
        res = self.client.get(driver_update_url)
        self.assertNotEquals(res.status_code, 200)
