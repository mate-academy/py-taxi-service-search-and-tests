from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

from taxi.models import Manufacturer, Car

MANUFACTURER_URL = reverse("taxi:manufacturer-list")
CAR_URL = reverse("taxi:car-list")
DRIVER_URL = reverse("taxi:driver-list")
PAGINATE_BY = 5


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

        number_of_manufacturers = 7
        for manufacturer in range(number_of_manufacturers):
            Manufacturer.objects.create(
                name="Test%s" % manufacturer,
                country="USA",
            )

    def test_retrieve_manufacturers(self):

        response = self.client.get(MANUFACTURER_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html",
        )
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.all())[:PAGINATE_BY]
        )

    def test_pagination_manufacturers(self):

        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?page=2"
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.all())[PAGINATE_BY:]
        )

    def test_search_manufacturer(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=test1"
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.filter(name__icontains="test1"))
        )

        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?name=test&page=2"
        )
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(
                Manufacturer.objects.filter(name__icontains="test")
            )[PAGINATE_BY:]
        )


class PublicCarTest(TestCase):
    def test_login_required(self):
        response = self.client.get(CAR_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            country="USA",
        )

        number_of_cars = 7
        for car in range(number_of_cars):
            Car.objects.create(
                model="Test%s" % car,
                manufacturer=manufacturer,
            )

    def test_retrieve_cars(self):

        response = self.client.get(CAR_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/car_list.html",
        )
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.all())[:PAGINATE_BY]
        )

    def test_pagination_cars(self):

        response = self.client.get(reverse("taxi:car-list") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.all())[PAGINATE_BY:]
        )

    def test_search_car(self):
        response = self.client.get(reverse("taxi:car-list") + "?model=test1")
        self.assertEqual(
            list(response.context["car_list"]),
            list(Car.objects.filter(model__icontains="test1"))
        )

        response = self.client.get(
            reverse("taxi:car-list") + "?model=test&page=2"
        )
        self.assertEqual(
            list(response.context["car_list"]),
            list(
                Car.objects.filter(model__icontains="test")
            )[PAGINATE_BY:]
        )


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(DRIVER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="test",
            password="test123",
        )
        self.client.force_login(self.admin_user)

        number_of_drivers = 7
        for driver in range(number_of_drivers):
            get_user_model().objects.create_user(
                username="Test%s" % driver,
                password="test_driver%s" % driver,
                license_number="ABC1234%s" % driver
            )

    def test_retrieve_drivers(self):

        response = self.client.get(DRIVER_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/driver_list.html",
        )
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(
            list(response.context["driver_list"]),
            list(get_user_model().objects.all())[:PAGINATE_BY]
        )

    def test_pagination_drivers(self):

        response = self.client.get(reverse("taxi:driver-list") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(
            list(response.context["driver_list"]),
            list(get_user_model().objects.all())[PAGINATE_BY:]
        )

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "user1test",
            "password2": "user1test",
            "first_name": "test first",
            "last_name": "test last",
            "license_number": "ABC12349",
        }
        self.client.post(reverse("taxi:driver-create"), form_data)
        new_driver = get_user_model().objects.get(
            username=form_data["username"]
        )
        self.assertEqual(new_driver.first_name, form_data["first_name"])
        self.assertEqual(new_driver.last_name, form_data["last_name"])
        self.assertEqual(
            new_driver.license_number,
            form_data["license_number"]
        )

    def test_search_driver(self):
        response = self.client.get(
            reverse("taxi:driver-list") + "?username=test1"
        )
        self.assertEqual(
            list(response.context["driver_list"]),
            list(get_user_model().objects.filter(username__icontains="test1"))
        )

        response = self.client.get(
            reverse("taxi:driver-list") + "?username=test&page=2"
        )
        self.assertEqual(
            list(response.context["driver_list"]),
            list(
                get_user_model().objects.filter(username__icontains="test")
            )[PAGINATE_BY:]
        )
