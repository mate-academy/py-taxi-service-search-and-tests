from django.test import TestCase, Client


MANUFACTURER_LIST_URL = "taxi:manufacturer-list"
CAR_LIST_URL = "taxi:car-list"
MANUFACTURER_CREATE_URL = "taxi:manufacturer-create"
CAR_CREATE_URL = "taxi:car-create"


class PublicTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_login_required_manuf_list(self):
        res = self.client.get(MANUFACTURER_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_manuf_create(self):
        res = self.client.get(MANUFACTURER_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_list(self):
        res = self.client.get(CAR_LIST_URL)
        self.assertNotEqual(res.status_code, 200)

    def test_login_required_car_create(self):
        res = self.client.get(CAR_CREATE_URL)
        self.assertNotEqual(res.status_code, 200)
