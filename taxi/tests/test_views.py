from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Car, Manufacturer

URL_PATHS = [
    "taxi:index",
    "taxi:car-list",
    "taxi:driver-list",
    "taxi:manufacturer-list"
]
URLS_NAME = [
    "car",
    "driver",
    "manufacturer",
]


class PublicUrlsTest(TestCase):
    def test_login_required(self):
        for path in URL_PATHS:
            res = self.client.get(reverse(path))
            self.assertNotEqual(res.status_code, 200)


class TemplatesViewTest(TestCase):
    def setUp(self):
        time = 7
        for num in range(1, time + 1):
            Driver.objects.create_user(
                username=f"testusername-{num}",
                password=f"testpassword-{num}",
                license_number=f"{num}{num}{num}AAAAA"
            )
            Manufacturer.objects.create(
                name=f"testname-{num}",
                country=f"testcountry-{num}",
            )
            Car.objects.create(
                model=f"testmodel-{num}",
                manufacturer_id=num,
            )
        user = get_user_model().objects.get(pk=1)
        self.client.force_login(user)

    def test_pagination_is_five(self):
        for url in URLS_NAME:
            response = self.client.get(reverse(f"taxi:{url}-list"))
            self.assertTrue("is_paginated" in response.context)
            self.assertTrue(response.context["is_paginated"])
            self.assertEqual(len(response.context[f"{url}_list"]), 5)

    def test_lists_all_objects_at_second_page(self):
        for url in URLS_NAME:
            response = self.client.get(reverse(f"taxi:{url}-list") + "?page=2")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.context[f"{url}_list"]), 2)
