from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer


CarListPath = reverse("taxi:car-list")
ManufacturerListPath = reverse("taxi:manufacturer-list")
ManufacturerCreateViewPath = reverse("taxi:manufacturer-create")


class PrivateManufacturerListViewTest(TestCase):
    def setUp(self) -> None:
        self.test_user = get_user_model().objects.create_user(
            username="test_user",
            password="test1234ABST"
        )
        self.client.force_login(self.test_user)

    def test_url_accessable_if_logged_in(self):
        response = self.client.get(ManufacturerListPath)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(ManufacturerListPath)
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

    def test_context_data(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Fiat", country="Italy")
        manufacturers = Manufacturer.objects.all()
        response = self.client.get(ManufacturerListPath)

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers)
        )

    def test_search_by_name(self):
        for i in range(10):
            Manufacturer.objects.create(
                name="Fiat" + str(i),
                country="Italy",
            )
        Manufacturer.objects.create(
            name="BMW",
            country="Germany"
        )
        response = self.client.get(
            ManufacturerListPath,
            data={"name": "BMW"}
        )
        expected_search_result = Manufacturer.objects.filter(
            name__icontains="BMW"
        )

        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(expected_search_result)
        )


class PublicManufacturerListViewTest(TestCase):
    def test_url_not_accessible(self):
        response = self.client.get(ManufacturerListPath)

        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerCreateViewTest(TestCase):
    def setUp(self) -> None:
        test_user = get_user_model().objects.create_user(
            username="test_user",
            password="test12345"
        )
        self.client.force_login(test_user)

    def test_url_accessible(self):
        response = self.client.get(ManufacturerCreateViewPath)

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(ManufacturerCreateViewPath)

        self.assertTemplateUsed(response, "taxi/manufacturer_form.html")

    def test_view_redirect(self):
        manufacturer_data = {
            "name": "Test firm",
            "country": "Test country"
        }
        response = self.client.post(
            ManufacturerCreateViewPath,
            data=manufacturer_data
        )

        self.assertRedirects(response, reverse("taxi:manufacturer-list"))


class PublicManufacturerCreateViewTest(TestCase):
    def test_url_not_accessible(self):
        response = self.client.get(ManufacturerCreateViewPath)

        self.assertNotEqual(response.status_code, 200)


class PrivateCarListViewTest(TestCase):
    def setUp(self) -> None:
        test_user = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.force_login(test_user)

    def test_url_accessible_if_logged_in(self):
        response = self.client.get(CarListPath)

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(CarListPath)

        self.assertTemplateUsed(response, "taxi/car_list.html")

    def test_context_data(self):
        manufacturer = Manufacturer.objects.create(
            name="Fiat",
            country="Italy"
        )
        driver = get_user_model().objects.create_user(
            username="test_user2",
            password="test1234abta",
            license_number="ABC12345"
        )
        car1 = Car.objects.create(model="test1", manufacturer=manufacturer)
        car1.drivers.add(driver)
        car2 = Car.objects.create(model="test2", manufacturer=manufacturer)
        car2.drivers.add(driver)
        cars = Car.objects.all()
        response = self.client.get(CarListPath)

        self.assertEqual(
            list(response.context["car_list"]),
            list(cars)
        )


class PublicCarListTest(TestCase):
    def test_url_not_accessible(self):
        response = self.client.get(CarListPath)

        self.assertNotEqual(response.status_code, 200)
