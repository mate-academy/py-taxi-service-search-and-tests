from django.contrib.auth.password_validation import password_changed
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from taxi.models import Car, Manufacturer


class DriverListViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="TestUser",
            password="password1",
            license_number="UKJ65641"
        )
        self.client.login(username="TestUser", password="password1")

        manufacturer_1 = Manufacturer.objects.create(
            name="Manufacturer_1",
            country="USA"
        )
        manufacturer_2 = Manufacturer.objects.create(
            name="Manufacturer_2",
            country="USA"
        )

        car_1 = Car.objects.create(model="Model3", manufacturer=manufacturer_1)
        car_2 = Car.objects.create(model="Model2", manufacturer=manufacturer_1)

        self.user.cars.add(car_1)

    def test_model_car_driver_detail(self):
        url = reverse("taxi:driver-detail", kwargs={"pk": self.user.pk})
        response = self.client.get(url)
        self.assertContains(response, "Model3")
        self.assertNotContains(response, "Model2")

    def test_search_bar_driver_list(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, {"search": "TestUser"})

        self.assertContains(response, self.user.license_number)

    def test_search_no_result1(self):
        url = reverse("taxi:driver-list")
        response = self.client.get(url, data={"search": "NotExistsUser"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["driver_list"]), 0)

    def test_logout_user_access(self):
        self.client.logout()

        url = reverse("taxi:driver-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_template_use(self):
        url = reverse("taxi:driver-detail", kwargs={"pk": self.user.pk})
        response = self.client.get(url)

        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_pagination(self):
        for i in range(0, 10):
            get_user_model().objects.create(
                username=f"User{i}",
                password="password",
                license_number=f"JKU7766{i}"
            )

        url = reverse("taxi:driver-list")
        response = self.client.get(url)
        response_2 = self.client.get(url, data={"page": 2})

        self.assertEqual(len(response.context["driver_list"]), 5)
        self.assertEqual(len(response_2.context["driver_list"]), 5)


class IndexTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="TestUser1",
            password="password2",
            license_number="UKJ65642"
        )
        self.client.login(username="TestUser1", password="password2")

    def test_num_visit_page(self):
        url = reverse("taxi:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.client.session["num_visits"], 1)

        self.client.get(url)
        self.assertEqual(self.client.session["num_visits"], 2)


class ToggleAssignToCar(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Testowy1",
            password="password1",
            license_number="IKL77551"
        )
        self.client.login(
            username="Testowy1",
            password="password1"
        )

    def test_toggle_assign_to_car1(self):
        manufacturer = Manufacturer.objects.create(
            name="Name",
            country="Poland"
        )
        car_1 = Car.objects.create(model="ModelS", manufacturer=manufacturer)

        url = reverse("taxi:toggle-car-assign", kwargs={"pk":car_1.pk})
        response = self.client.post(url)

        self.assertRedirects(response, reverse("taxi:car-detail", kwargs={"pk":car_1.pk}))

        self.assertTrue(self.user.cars.filter(id=car_1.pk).exists())

        self.client.post(url)
        self.assertFalse(self.user.cars.filter(id=car_1.pk).exists())

