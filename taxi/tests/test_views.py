from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Car


class ManufacturerViewTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        get_user_model().objects.create_user(
            username="user1",
            password="qwerty"
        )
        for number in range(10):
            Manufacturer.objects.create(
                name="BMW" + str(number),
                country="Germany"
            )

    def setUp(self) -> None:
        self.user = get_user_model().objects.get(id=1)

    def test_login_required_for_unauthorized_users(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/manufacturers/")

    def test_retrieve_all_manufacturers(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.all()[:5])
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_search_field_manufacturers(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": "BMW0"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            [Manufacturer.objects.get(name="BMW0")]
        )

    def test_pagination(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("taxi:manufacturer-list"))

        self.assertEqual(len(response.context["manufacturer_list"]), 5)

    def test_if_all_manufacturers_when_there_is_no_search(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("taxi:manufacturer-list"), {"name": ""}
        )

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(Manufacturer.objects.all()[:5])
        )

    def test_invalid_search(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"name": "NonExistentManufacturer"}
        )

        self.assertEqual(list(response.context["manufacturer_list"]), [])

    def test_create_manufacturer(self):
        self.client.force_login(self.user)

        data = {
            "name": "Audi",
            "country": "Germany",
        }

        response = self.client.post(
            reverse("taxi:manufacturer-create"), data=data
        )

        self.assertRedirects(response, reverse("taxi:manufacturer-list"))
        self.assertTrue(Manufacturer.objects.filter(name="Audi").exists())

    def test_create_manufacturer_without_login(self):
        data = {
            "name": "Audi",
            "country": "Germany",
        }

        response = self.client.post(
            reverse("taxi:manufacturer-create"), data=data
        )

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response, "/accounts/login/?next=/manufacturers/create/"
        )
        self.assertFalse(Manufacturer.objects.filter(name="Audi").exists())

    def test_update_manufacturer(self):
        self.client.force_login(self.user)

        data = {
            "name": "Mercedes",
            "country": "Germany",
        }
        self.manufacturer = Manufacturer.objects.get(id=1)

        response = self.client.post(
            reverse("taxi:manufacturer-update", args=[self.manufacturer.id]),
            data=data
        )

        self.assertRedirects(response, reverse("taxi:manufacturer-list"))

        self.manufacturer.refresh_from_db()
        self.assertEqual(self.manufacturer.name, "Mercedes")
        self.assertEqual(self.manufacturer.country, "Germany")


class ToggleAssignToCarTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="user",
            password="qwerty",
            license_number="ZXC12345",
        )
        self.user2 = get_user_model().objects.create_user(
            username="user2",
            password="asdf",
            license_number="QWE12345",
        )
        self.client.force_login(self.user)

        manufacturer = Manufacturer.objects.create(
            name="Audi Motors",
            country="German"
        )
        self.car = Car.objects.create(model="BMW", manufacturer=manufacturer)
        self.car.drivers.set([self.user2])

    def test_toggle_assign_to_existing_car(self):
        self.user.cars.add(self.car)

        self.client.get(reverse("taxi:toggle-car-assign", args=[self.car.id]))

        self.assertNotIn(self.car, self.user.cars.all())

    def test_toggle_assign_to_non_existing_car(self):
        initial_car_count = self.user.cars.count()

        self.client.get(reverse("taxi:toggle-car-assign", args=[self.car.id]))

        self.assertNotEqual(initial_car_count, self.user.cars.count())

    def test_toggle_assign_to_new_car(self):
        self.client.get(reverse("taxi:toggle-car-assign", args=[self.car.id]))

        self.assertIn(self.car, self.user.cars.all())

    def test_redirect_after_toggle(self):
        car_detail_url = reverse("taxi:car-detail", args=[self.car.id])

        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.id])
        )

        self.assertRedirects(response, car_detail_url)
