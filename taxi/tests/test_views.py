from django.test import TestCase
from django.urls import reverse

CAR_URL = reverse("taxi:car-list")
CAR_DETAIL_URL = reverse("taxi:car-detail", kwargs={"pk": 1})
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVER_URL = reverse("taxi:driver-list")
DRIVER_DETAIL_URL = reverse("taxi:driver-detail", kwargs={"pk": 1})


class PublicTests(TestCase):
    def test_login_required(self):
        response_car_list = self.client.get(CAR_URL)
        response_car_detail = self.client.get(CAR_DETAIL_URL)
        response_manufacturer_list = self.client.get(MANUFACTURER_URL)
        response_driver_list = self.client.get(DRIVER_URL)
        response_driver_detail = self.client.get(DRIVER_DETAIL_URL)
        self.assertNotEqual(response_car_list.status_code, 200)
        self.assertNotEqual(response_car_detail.status_code, 200)
        self.assertNotEqual(response_manufacturer_list.status_code, 200)
        self.assertNotEqual(response_driver_list.status_code, 200)
        self.assertNotEqual(response_driver_detail.status_code, 200)
