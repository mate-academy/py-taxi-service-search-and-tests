from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.forms import ManufacturersSearchForm, CarSearchForm
from taxi.models import Manufacturer, Car


class PublicDriverViewsTest(TestCase):
    def test_login_required_manufacturer_list_view(self):
        manufacturer_list_url = reverse("taxi:manufacturer-list")
        response = self.client.get(manufacturer_list_url)

        self.assertNotEquals(response.status_code, 200)

    #
    def test_login_required_car_list_view(self):
        car_list_url = reverse("taxi:car-list")
        response = self.client.get(car_list_url)

        self.assertNotEquals(response.status_code, 200)

    def test_login_required_driver_list_view(self):
        driver_list_url = reverse("taxi:driver-list")
        response = self.client.get(driver_list_url)

        self.assertNotEquals(response.status_code, 200)


class PrivateDriverViewsTest(TestCase):
    def setUp(self):
        for num in range(8):
            get_user_model().objects.create_user(
                username=f"testusername{num}",
                first_name=f"First name Test{num}",
                last_name=f"Last name Test{num}",
                password=f"123testadmin{num}",
                license_number=f"AAA1111{num}"
            )

        self.client.force_login(get_user_model().objects.get(id=1))

        for num in range(8):
            Manufacturer.objects.create(
                name=f"manufacturer-test#{num}",
                country=f"country-test#{num}"
            )
        for car_num in range(8):
            Car.objects.create(
                model=f"Test car# {car_num}",
                manufacturer=Manufacturer.objects.get(id=1)
            )

    def test_retrieve_car_list(self):
        car_list_url = reverse("taxi:car-list")
        response = self.client.get(car_list_url)

        cars = Car.objects.all()[:5]

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["car_list"]),
            list(cars)
        )
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_retrieve_manufacturer_list(self):
        manufacturer_list_url = reverse("taxi:manufacturer-list")
        response = self.client.get(manufacturer_list_url)

        manufacturer = Manufacturer.objects.all()[:5]

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["manufacturer_list"]),
            list(manufacturer)
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_create_author_in_db(self):
        form_data = {
            "username": "testusername0",
            "first_name": "First name Test0",
            "last_name": "Last name Test0",
            "password1": "123testadmin0",
            "password2": "123testadmin0",
            "license_number": "AAA11110"
        }

        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(id=1)

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_car_list_pagination_is_five(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_manufacturer_list_pagination_is_five(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_driver_list_pagination_is_five(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_search_manufacturer_using_form(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")

        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"title": "Toyota"}
        )
        form = ManufacturersSearchForm({"title": "Toyota"})
        expected_queryset = Manufacturer.objects.filter(
            name__icontains="Toyota"
        )

        self.assertTrue(form.is_valid())
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["manufacturer_list"]),
            list(expected_queryset)
        )

    def test_search_car_using_form(self):
        Car.objects.create(
            model="Mustang",
            manufacturer=Manufacturer.objects.get(id=1)
        )

        response = self.client.get(
            reverse("taxi:car-list"), {"title": "Mustang"}
        )
        form = CarSearchForm({"title": "Mustang"})
        expected_queryset = Car.objects.select_related(
            "manufacturer"
        ).filter(model__icontains="Mustang")

        self.assertTrue(form.is_valid())
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["car_list"]),
            list(expected_queryset)
        )

    def test_search_driver_using_form(self):
        get_user_model().objects.create_user(
            username="UserForTest",
            password="123testadmin123",

        )

        response = self.client.get(
            reverse("taxi:driver-list"), {"title": "UserForTest"}
        )
        form = CarSearchForm({"title": "UserForTest"})
        expected_queryset = get_user_model().objects.filter(
            username__icontains="UserForTest")

        self.assertTrue(form.is_valid())
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            list(response.context["driver_list"]),
            list(expected_queryset)
        )
