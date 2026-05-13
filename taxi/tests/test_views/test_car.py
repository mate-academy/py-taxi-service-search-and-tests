from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from taxi.models import Car, Manufacturer


class PublicCarListViewTest(TestCase):
    def test_login_required_redirects_anonymous_user(self):
        url = reverse("taxi:car-list")
        response = self.client.get(url)
        self.assertRedirects(response, f"{reverse('login')}?next={url}")


class PrivateCarListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.user = user_model.objects.create_user(
            username="test",
            password="test12345",
            first_name="first_test",
            last_name="last_test",
            license_number="ABC12345",
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )
        cls.car_1 = Car.objects.create(
            model="test_model1",
            manufacturer=cls.manufacturer
        )
        cls.car_2 = Car.objects.create(
            model="test_model2",
            manufacturer=cls.manufacturer
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_logged_in_user_can_access_page(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertIn(self.car_1, response.context["car_list"])
        self.assertIn(self.car_2, response.context["car_list"])

    def test_search_cars_by_model(self):
        response = self.client.get(reverse("taxi:car-list"), {"q": "model2"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_list.html")
        self.assertIn(self.car_2, response.context["car_list"])
        self.assertNotIn(self.car_1, response.context["car_list"])


class PublicCarDetailViewTest(TestCase):
    def test_login_required_redirects_anonymous_user(self):
        manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )
        car = Car.objects.create(
            model="test_model1",
            manufacturer=manufacturer
        )
        url = reverse("taxi:car-detail", args=[car.pk])
        response = self.client.get(url)
        self.assertRedirects(response, f"{reverse('login')}?next={url}")


class PrivateCarDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.user = user_model.objects.create_user(
            username="test",
            password="test12345",
            first_name="first_test",
            last_name="last_test",
            license_number="ABC12345",
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )
        cls.car = Car.objects.create(
            model="test_model1",
            manufacturer=cls.manufacturer
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_logged_in_user_can_access_page(self):
        url = reverse("taxi:car-detail", args=[self.car.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/car_detail.html")
        self.assertEqual(response.context["object"], self.car)


class PublicCarCreateViewTest(TestCase):
    def test_login_required_redirects_anonymous_user(self):
        url = reverse("taxi:car-create")
        response = self.client.get(url)
        self.assertRedirects(response, f"{reverse('login')}?next={url}")


class PrivateCarCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.user = user_model.objects.create_user(
            username="test",
            password="test12345",
            first_name="first_test",
            last_name="last_test",
            license_number="ABC12345",
        )
        cls.manufacturer = Manufacturer.objects.create(
            name="test_manufacturer",
            country="test_country"
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_logged_in_user_can_create_car(self):
        url = reverse("taxi:car-create")
        response = self.client.post(
            url,
            data={"model": "test_model1",
                  "manufacturer": self.manufacturer.pk,
                  "drivers": [self.user.pk]
                  }
        )
        self.assertRedirects(response, reverse("taxi:car-list"))
        self.assertEqual(Car.objects.count(), 1)
