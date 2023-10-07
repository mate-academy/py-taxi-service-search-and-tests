from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


class ManufacturerViewTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        manufacturers_num = 14

        get_user_model().objects.create_user(  # type: ignore
            username="test_user", password="test_password"
        )

        for manufacturer_id in range(manufacturers_num):
            Manufacturer.objects.create(
                name=f"test_name_{manufacturer_id}",
                country="test_country",
            )

    def test_manufacturer_list_redirect_if_not_logged_in(self) -> None:
        resp = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertRedirects(
            resp,
            "/accounts/login/?next=/manufacturers/",
        )

    def test_manufacturer_list_if_logged_in(self) -> None:
        test_user = get_user_model().objects.get(pk=1)
        self.client.force_login(test_user)
        resp = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(resp.context["user"].pk, test_user.pk)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "taxi/manufacturer_list.html")

    def test_manufacturer_list_pagination(self) -> None:
        test_user = get_user_model().objects.get(pk=1)
        self.client.force_login(test_user)
        resp = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(resp.status_code, 200)
        self.assertTrue("is_paginated" in resp.context)
        self.assertEqual(resp.context["is_paginated"], True)
        self.assertEqual(len(resp.context["manufacturer_list"]), 5)

    def test_manufacturer_list_pagination_last_page(self) -> None:
        test_user = get_user_model().objects.get(pk=1)
        self.client.force_login(test_user)
        resp = self.client.get(reverse("taxi:manufacturer-list") + "?page=3")

        self.assertEqual(resp.status_code, 200)
        self.assertTrue("is_paginated" in resp.context)
        self.assertEqual(resp.context["is_paginated"], True)
        self.assertEqual(len(resp.context["manufacturer_list"]), 4)

    def test_manufacturer_list_search(self) -> None:
        search_param = "test_name_13"

        test_user = get_user_model().objects.get(pk=1)
        self.client.force_login(test_user)
        resp = self.client.get(
            reverse("taxi:manufacturer-list") + f"?name={search_param}"
        )
        filtered_manufacturers = Manufacturer.objects.filter(
            name__icontains=search_param
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context["manufacturer_list"]), 1)
        self.assertEqual(
            list(resp.context["manufacturer_list"]),
            list(filtered_manufacturers),
        )


class TestCarDriverUpdateView(TestCase):
    def setUp(self) -> None:
        self.test_user = get_user_model().objects.create_user(  # type: ignore
            username="test_user", password="test_password"
        )
        test_manufacturer = Manufacturer.objects.create(
            name="test_manufacturer", country="test_country"
        )
        self.test_car = Car.objects.create(
            model="test_model", manufacturer=test_manufacturer
        )

    def test_car_driver_is_assigned(self) -> None:
        self.client.force_login(self.test_user)

        self.client.post(
            reverse("taxi:car-update-driver", kwargs={"pk": self.test_car.pk})
        )

        self.assertEqual(list(self.test_car.drivers.all()), [self.test_user])

    def test_car_driver_is_removed(self) -> None:
        self.client.force_login(self.test_user)

        self.test_car.drivers.add(self.test_user)
        self.client.post(
            reverse("taxi:car-update-driver", kwargs={"pk": self.test_car.pk})
        )

        self.assertEqual(list(self.test_car.drivers.all()), [])
