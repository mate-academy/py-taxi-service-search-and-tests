from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Driver, Car, Manufacturer

User = get_user_model()


class IndexViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password")
        self.client = Client()

    def test_index_requires_login(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertRedirects(response, "/accounts/login/?next=/")

    def test_index_displays_counts(self):
        self.client.login(username="testuser", password="password")

        Manufacturer.objects.create(name="Audi", country="Germany")
        Manufacturer.objects.create(name="BMW", country="Germany")
        Car.objects.create(
            model="A6", manufacturer=Manufacturer.objects.first())
        Driver.objects.create_user(
            username="driver2", password="pass123", license_number="ABC12345"
        )

        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/index.html")

        self.assertEqual(response.context["num_drivers"], 2)
        self.assertEqual(response.context["num_cars"], 1)
        self.assertEqual(response.context["num_manufacturers"], 2)


class ManufacturerListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(13):
            Manufacturer.objects.create(
                name=f"Manuf_{i}", country="Country_{i}")

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password")
        self.client.login(username="testuser", password="password")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/manufacturers/")
        self.assertEqual(response.status_code, 200)

    def test_view_accessible_by_name(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_pagination_by_5(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_second_page_has_remaining_8(self):
        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?page=2")
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["manufacturer_list"]), 5)

        response = self.client.get(
            reverse("taxi:manufacturer-list") + "?page=3")
        self.assertEqual(len(response.context["manufacturer_list"]), 3)

    def test_search_filter(self):
        Manufacturer.objects.create(name="TestSearch", country="USA")
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"query": "TestSearch"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["manufacturer_list"]), 1)
        self.assertContains(response, "TestSearch")


class CarListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create(
            name="Audi", country="Germany")
        for i in range(7):
            Car.objects.create(model=f"Model_{i}", manufacturer=manufacturer)

    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pass")
        self.client.login(username="user", password="pass")

    def test_car_list_view(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")

        self.assertEqual(len(response.context["car_list"]), 5)

    def test_second_page_list(self):
        response = self.client.get(reverse("taxi:car-list") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["car_list"]), 2)

    def test_search_car_model(self):
        Car.objects.create(
            model="SPECIAL_SEARCH", manufacturer=Manufacturer.objects.first()
        )
        response = self.client.get(
            reverse("taxi:car-list"), {"query": "SPECIAL_SEARCH"}
        )
        self.assertEqual(len(response.context["car_list"]), 1)


class CarDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pass")
        self.client.login(username="user", password="pass")

        self.manufacturer = Manufacturer.objects.create(
            name="Audi", country="Germany")
        self.car = Car.objects.create(
            model="A4", manufacturer=self.manufacturer)

    def test_car_detail_view(self):
        response = self.client.get(
            reverse("taxi:car-detail", kwargs={"pk": self.car.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")
        self.assertEqual(response.context["car"], self.car)


class DriverListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Driver.objects.all().delete()
        for i in range(6):
            Driver.objects.create_user(
                username=f"driver{i}",
                password="pass123",
                license_number=f"ABC{1000 + i}",
            )

    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pass")
        self.client.login(username="user", password="pass")

    def test_driver_list_view(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertEqual(len(response.context["driver_list"]), 1)

    def test_pagination(self):
        response = self.client.get(reverse("taxi:driver-list") + "?page=2")
        self.assertEqual(len(response.context["driver_list"]), 1)

    def test_search_driver(self):
        response = self.client.get(
            reverse("taxi:driver-list"), {"query": "driver3"})
        self.assertEqual(len(response.context["driver_list"]), 1)


class DriverDetailViewTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="driver99", password="pass123", license_number="ABC99999"
        )
        self.user = User.objects.create_user(username="user", password="pass")
        self.client.login(username="user", password="pass")

    def test_driver_detail_view(self):
        response = self.client.get(
            reverse("taxi:driver-detail", kwargs={"pk": self.driver.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")
        self.assertEqual(response.context["driver"], self.driver)


class DriverCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pass")
        self.client.login(username="user", password="pass")

    def test_create_driver_success(self):
        form_data = {
            "username": "newdriver",
            "password1": "mycomplexpassword123",
            "password2": "mycomplexpassword123",
            "license_number": "ABC12345",
            "first_name": "Jane",
            "last_name": "Doe",
        }
        response = self.client.post(
            reverse("taxi:driver-create"), data=form_data)
        self.assertEqual(response.status_code, 302)

        self.assertTrue(Driver.objects.filter(username="newdriver").exists())

    def test_create_driver_invalid_license_number(self):
        form_data = {
            "username": "driver2",
            "password1": "testpass123",
            "password2": "testpass123",
            "license_number": "ABCD1111",
            "first_name": "Jane",
            "last_name": "Doe",
        }
        response = self.client.post(
            reverse("taxi:driver-create"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Driver.objects.filter(username="driver2").exists())
        form_errors = response.context["form"].errors.get("license_number", [])
        self.assertIn("Last 5 characters should be digits", form_errors)


class ToggleAssignToCarTest(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="driver1", password="pass123", license_number="ABC12345"
        )
        self.manufacturer = Manufacturer.objects.create(
            name="Volvo", country="Sweden")
        self.car = Car.objects.create(
            model="XC90", manufacturer=self.manufacturer)
        self.client.login(username="driver1", password="pass123")

    def test_assign_car_to_driver(self):
        self.assertEqual(self.user.cars.count(), 0)

        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.pk])
        )
        self.assertRedirects(
            response, reverse("taxi:car-detail", args=[self.car.pk]))
        self.user.refresh_from_db()
        self.assertEqual(self.user.cars.count(), 1)

    def test_unassign_car_from_driver(self):
        self.user.cars.add(self.car)
        self.assertEqual(self.user.cars.count(), 1)

        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.pk])
        )
        self.assertRedirects(
            response, reverse("taxi:car-detail", args=[self.car.pk]))
        self.user.refresh_from_db()
        self.assertEqual(self.user.cars.count(), 0)
