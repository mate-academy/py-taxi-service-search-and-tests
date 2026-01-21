from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Car, Manufacturer

User = get_user_model()


class SearchViewsTests(TestCase):
    def setUp(self):
        # виробники
        self.m1 = Manufacturer.objects.create(name="Toyota", country="JP")
        self.m2 = Manufacturer.objects.create(name="Ford", country="US")
        self.m3 = Manufacturer.objects.create(name="Tesla", country="US")

        # авто
        self.car1 = Car.objects.create(model="Corolla", manufacturer=self.m1)
        self.car2 = Car.objects.create(model="Mustang", manufacturer=self.m2)
        self.car3 = Car.objects.create(model="Model S", manufacturer=self.m3)

        # водії
        self.d1 = User.objects.create_user(
            username="alice", password="pass1234", license_number="ABC12345"
        )
        self.d2 = User.objects.create_user(
            username="bob", password="pass1234", license_number="DEF12345"
        )
        self.d3 = User.objects.create_user(
            username="alex", password="pass1234", license_number="GHI12345"
        )

        # логін для доступу до захищених сторінок
        self.client.force_login(self.d1)

    def test_driver_list_search(self):
        url = reverse("taxi:driver-list")

        # без фільтра – всі
        rr = self.client.get(url)
        self.assertEqual(rr.status_code, 200)
        self.assertQuerysetEqual(
            rr.context["object_list"],
            [self.d1, self.d2, self.d3],
            transform=lambda x: x,
            ordered=False,
        )

        # 'al' → alice + alex
        rr = self.client.get(url, {"username": "al"})
        self.assertQuerysetEqual(
            rr.context["object_list"],
            [self.d1, self.d3],
            transform=lambda x: x,
            ordered=False,
        )

        # 'bob' → лише bob
        rr = self.client.get(url, {"username": "bob"})
        self.assertQuerysetEqual(
            rr.context["object_list"], [self.d2], transform=lambda x: x
        )

        # нічого не знайдено
        rr = self.client.get(url, {"username": "zzz"})
        self.assertEqual(list(rr.context["object_list"]), [])

    def test_car_list_search(self):
        url = reverse("taxi:car-list")

        # без фільтра – всі
        rr = self.client.get(url)
        self.assertEqual(rr.status_code, 200)
        self.assertQuerysetEqual(
            rr.context["object_list"],
            [self.car1, self.car2, self.car3],
            transform=lambda x: x,
            ordered=False,
        )

        # 'mo' → тільки Model S
        rr = self.client.get(url, {"model": "mo"})
        self.assertQuerysetEqual(
            rr.context["object_list"], [self.car3], transform=lambda x: x
        )

        # 'mu' → лише Mustang
        rr = self.client.get(url, {"model": "mu"})
        self.assertQuerysetEqual(
            rr.context["object_list"], [self.car2], transform=lambda x: x
        )

        # 'Corolla' → Corolla
        rr = self.client.get(url, {"model": "Corolla"})
        self.assertQuerysetEqual(
            rr.context["object_list"], [self.car1], transform=lambda x: x
        )

        # нічого не знайдено
        rr = self.client.get(url, {"model": "X5"})
        self.assertEqual(list(rr.context["object_list"]), [])

    def test_manufacturer_list_search(self):
        url = reverse("taxi:manufacturer-list")

        # без фільтра – всі
        rr = self.client.get(url)
        self.assertEqual(rr.status_code, 200)
        self.assertQuerysetEqual(
            rr.context["object_list"],
            [self.m1, self.m2, self.m3],
            transform=lambda x: x,
            ordered=False,
        )

        # 'to' → Toyota
        rr = self.client.get(url, {"name": "to"})
        self.assertQuerysetEqual(
            rr.context["object_list"], [self.m1], transform=lambda x: x
        )

        # 'fo' → Ford
        rr = self.client.get(url, {"name": "fo"})
        self.assertQuerysetEqual(
            rr.context["object_list"], [self.m2], transform=lambda x: x
        )

        # 'te' → Tesla
        rr = self.client.get(url, {"name": "te"})
        self.assertQuerysetEqual(
            rr.context["object_list"], [self.m3], transform=lambda x: x
        )

        # нічого не знайдено
        rr = self.client.get(url, {"name": "xxx"})
        self.assertEqual(list(rr.context["object_list"]), [])
