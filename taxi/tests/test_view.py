from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class PublicCarTests(TestCase):
    def setUp(self):
        manufacturer = Manufacturer.objects.create(name="Test", country="USA")
        self.car = Car.objects.create(
            model="Test Model",
            manufacturer=manufacturer
        )

    def test_login_required_list(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertRedirects(response, "/accounts/login/?next=/cars/")

    def test_login_required_detail(self):
        response = self.client.get(
            reverse("taxi:car-detail",
                    kwargs={"pk": self.car.pk})
        )
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/cars/{self.car.pk}/"
        )

    def test_login_required_create(self):
        response = self.client.get(reverse("taxi:car-create"))
        self.assertRedirects(
            response,
            "/accounts/login/?next=/cars/create/"
        )

    def test_login_required_delete(self):
        response = self.client.get(
            reverse("taxi:car-delete",
                    kwargs={"pk": self.car.pk})
        )
        self.assertRedirects(
            response,
            "/accounts/login/?next=/cars/1/delete/"
        )


class PrivateCarTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test12345"
        )
        self.client.force_login(self.user)
        manufacturer = Manufacturer.objects.create(
            name="Test",
            country="USA"
        )
        self.cars = []
        for i in range(7):
            car = Car.objects.create(
                model=f"Model {i}",
                manufacturer=manufacturer
            )
            self.cars.append(car)
        self.car = self.cars[0]

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

    def test_list_view(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/car_list.html"
        )

    def test_detail_view(self):
        response = self.client.get(
            reverse("taxi:car-detail",
                    kwargs={"pk": self.car.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.car.model)

    def test_delete_view_redirects(self):
        response = self.client.get(
            reverse("taxi:car-delete",
                    kwargs={"pk": self.car.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_create_view_get(self):
        response = self.client.get(reverse("taxi:car-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_form.html")

    def test_retrieve_cars(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_pagination_is_five(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["car_list"]), 5)

    def test_search_returns_correct_results(self):
        response = self.client.get(
            reverse("taxi:car-list"),
            {"model": "Model 1"}
        )
        self.assertContains(response, "Model 1")
        self.assertNotContains(response, "Model 2")


class PublicManufacturerTests(TestCase):
    def setUp(self):
        name = "Test"
        country = "USA"
        self.manufacturer = Manufacturer.objects.create(
            name=name,
            country=country
        )

    def test_login_required_list(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertRedirects(
            response, "/accounts/login/?next=/manufacturers/")

    def test_login_required_create(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertRedirects(
            response,
            "/accounts/login/?next=/manufacturers/create/"
        )

    def test_login_required_delete(self):
        response = self.client.get(

            reverse("taxi:manufacturer-delete",
                    kwargs={"pk": self.manufacturer.pk})
        )
        self.assertRedirects(
            response,
            "/accounts/login/?next=/manufacturers/1/delete/"
        )


class PrivateManufacturerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test12345"
        )
        self.client.force_login(self.user)

        self.manufacturers = []
        for i in range(7):
            manufacturer = Manufacturer.objects.create(
                name=f"Test {i}",
                country="USA"
            )
            self.manufacturers.append(manufacturer)
        self.manufacturer = self.manufacturers[0]

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_list_view(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )

    def test_delete_view_redirects(self):
        response = self.client.get(
            reverse("taxi:manufacturer-delete",
                    kwargs={"pk": self.manufacturer.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_create_view_get(self):
        response = self.client.get(reverse("taxi:manufacturer-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_form.html"
        )

    def test_retrieve_manufacturers(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "taxi/manufacturer_list.html"
        )

    def test_pagination_is_five(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_search_returns_correct_results(self):
        Manufacturer.objects.create(name="Tesla", country="USA")
        Manufacturer.objects.create(name="Ford", country="USA")
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "Tesla"}
        )
        self.assertContains(response, "Tesla")
        self.assertNotContains(response, "Ford")


class PublicDriverTests(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="Test",
            password="test",
            license_number="ABC12345"
        )

    def test_login_required_list(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertRedirects(
            response,
            "/accounts/login/?next=/drivers/"
        )

    def test_login_required_detail(self):
        response = self.client.get(
            reverse("taxi:driver-detail",
                    kwargs={"pk": self.driver.pk})
        )
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/drivers/{self.driver.pk}/"
        )

    def test_login_required_create(self):
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertRedirects(
            response,
            "/accounts/login/?next=/drivers/create/"
        )

    def test_login_required_delete(self):
        response = self.client.get(
            reverse("taxi:driver-delete",
                    kwargs={"pk": self.driver.pk})
        )
        self.assertRedirects(
            response,
            "/accounts/login/?next=/drivers/1/delete/"
        )


class PrivateDriverTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="test12345"
        )
        self.client.force_login(self.user)

        self.drivers = []
        for i in range(7):
            driver = get_user_model().objects.create_user(
                username=f"driver{i}",
                password="pass12345",
                license_number=f"ABC1234{i}"
            )
            self.drivers.append(driver)
        self.driver = self.drivers[0]

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)

    def test_list_view(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_detail_view(self):
        response = self.client.get(
            reverse("taxi:driver-detail",
                    kwargs={"pk": self.driver.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.driver.username)

    def test_delete_view(self):
        response = self.client.post(
            reverse("taxi:driver-delete",
                    kwargs={"pk": self.driver.pk})
        )
        self.assertRedirects(response, reverse("taxi:driver-list"))
        self.assertFalse(
            get_user_model().objects.filter(pk=self.driver.pk).exists()
        )

    def test_create_view_get(self):
        response = self.client.get(reverse("taxi:driver-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_pagination_is_five(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["driver_list"]), 5)

    def test_search_returns_correct_results(self):
        response = self.client.get(
            reverse("taxi:driver-list"),
            {"username": "driver1"}
        )
        self.assertContains(response, "driver1")
        self.assertNotContains(response, "driver2")
