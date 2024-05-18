from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_LIST_URL = "taxi:manufacturer-list"
CAR_LIST_URL = "taxi:car-list"
DRIVER_LIST_URL = "taxi:driver-list"


class PublicManufacturerListViewTest(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse(MANUFACTURER_LIST_URL))
        self.assertNotEqual(res.status_code, 200)


class PrivetManufacturerListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 manufacturers for pagination tests
        number_of_manufacturers = 8

        for manufacturer_id in range(number_of_manufacturers):
            Manufacturer.objects.create(
                name=f"Name {manufacturer_id}",
                country=f"Country {manufacturer_id}",
            )

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_response_template(self):
        response = self.client.get(reverse(MANUFACTURER_LIST_URL))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_pagination_is_5(self):
        response = self.client.get(reverse(MANUFACTURER_LIST_URL))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.all()[:5])
        )

    def test_list_all_manufacturers(self):
        response = self.client.get(reverse(MANUFACTURER_LIST_URL) + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["manufacturer_list"]), 3)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.all()[5:])
        )

    def test_view_search_form_in_context(self):
        response = self.client.get(reverse(MANUFACTURER_LIST_URL))
        self.assertTrue("search_form" in response.context)

    def test_search_form_on_queryset(self):
        search_query = "1"
        response = self.client.get(
            reverse(MANUFACTURER_LIST_URL),
            {"name": search_query}
        )
        self.assertEqual(response.status_code, 200)

        queryset = response.context["manufacturer_list"]
        filtered_queryset = Manufacturer.objects.filter(
            name__icontains=search_query
        )

        self.assertEqual(list(queryset), list(filtered_queryset))


class PublicCarListViewTest(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse(DRIVER_LIST_URL))
        self.assertNotEqual(res.status_code, 200)


class PrivetCarListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_manufacturers = 8

        for car_id in range(number_of_manufacturers):
            Car.objects.create(
                model=f"Car model {car_id}",
                manufacturer=Manufacturer.objects.create(
                    name=f"Manufacturer name {car_id}",
                    country=f"Manufacturer country {car_id}",
                ),
            )

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_response_template(self):
        response = self.client.get(reverse(CAR_LIST_URL))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_pagination_is_5(self):
        response = self.client.get(reverse(CAR_LIST_URL))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertTrue(len(response.context["car_list"]) == 5)
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.all()[:5])
        )

    def test_list_all_cars(self):
        response = self.client.get(reverse(CAR_LIST_URL) + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertTrue(len(response.context["car_list"]) == 3)
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.all()[5:])
        )

    def test_view_search_form_in_context(self):
        response = self.client.get(reverse(CAR_LIST_URL))
        self.assertTrue("search_form" in response.context)

    def test_search_form_on_queryset(self):
        model = "1"
        response = self.client.get(
            reverse(CAR_LIST_URL),
            {"model": model}
        )
        self.assertEqual(response.status_code, 200)

        queryset = response.context["car_list"]
        filtered_queryset = Car.objects.filter(
            model__icontains=model
        )

        self.assertEqual(
            list(queryset),
            list(filtered_queryset)
        )


class PublicDriverListViewTest(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse(CAR_LIST_URL))
        self.assertNotEqual(res.status_code, 200)


class PrivetDriverListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_drivers = 8

        for driver_id in range(number_of_drivers):
            get_user_model().objects.create_user(
                username=f"Driver{driver_id}",
                password="test123",
                license_number=f"ABC1234{driver_id}"
            )

    def setUp(self):
        self.client.force_login(get_user_model().objects.get(id=1))

    def test_response_template(self):
        res = self.client.get(reverse(DRIVER_LIST_URL))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "taxi/driver_list.html")

    def test_pagination_is_5(self):
        response = self.client.get(reverse(DRIVER_LIST_URL))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertTrue(len(response.context["driver_list"]) == 5)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(get_user_model().objects.all()[:5])
        )

    def test_list_all_cars(self):
        response = self.client.get(reverse(DRIVER_LIST_URL) + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertTrue(len(response.context["driver_list"]) == 3)
        self.assertEqual(
            list(response.context["driver_list"]),
            list(get_user_model().objects.all()[5:])
        )

    def test_view_search_form_in_context(self):
        response = self.client.get(reverse(DRIVER_LIST_URL))
        self.assertTrue("search_form" in response.context)

    def test_search_form_on_queryset(self):
        username = "1"
        response = self.client.get(
            reverse(DRIVER_LIST_URL),
            {"username": username}
        )
        self.assertEqual(response.status_code, 200)

        queryset = response.context["driver_list"]
        filtered_queryset = get_user_model().objects.filter(
            username__icontains=username
        )

        self.assertEqual(list(queryset), list(filtered_queryset))
