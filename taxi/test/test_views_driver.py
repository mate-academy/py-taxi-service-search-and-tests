from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class PublicDriverTest(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test_admin",
            password="<PASSWORD>",
            license_number="ABC00100",
        )
        self.user1 = get_user_model().objects.create_user(
            username="test_name_1",
            password="password123",
            license_number="AAA33033",
        )
        self.user2 = get_user_model().objects.create_user(
            username="test_name_2",
            password="password123",
            license_number="AAA22022",
        )
        self.client.force_login(self.user)
        self.drivers_list_url = reverse("taxi:driver-list")

    def test_retrieve_driver_list(self):
        response = self.client.get(self.drivers_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("driver_list", response.context)
        drivers = get_user_model().objects.all()
        self.assertEqual(list(response.context["driver_list"]), list(drivers))
        self.assertTemplateUsed(response, "taxi/driver_list.html")

    def test_retrieve_driver_detail(self):
        url = reverse("taxi:driver-detail", kwargs={"pk": self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("driver", response.context)
        self.assertEqual(response.context["driver"], self.user)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")

    def test_create_driver(self):
        form_data = {
            "username": "new_user",
            "password1": "Strongpassword111",
            "password2": "Strongpassword111",
            "first_name": "New",
            "last_name": "User",
            "license_number": "ABC55055",
        }
        self.client.post(reverse("taxi:driver-create"), data=form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.license_number, form_data["license_number"])

    def test_update_driver_license_number(self):
        form_data = {"license_number": "XXX99099"}
        url = reverse("taxi:driver-update", kwargs={"pk": self.user.id})
        response = self.client.post(url, data=form_data)

        self.user.refresh_from_db()
        self.assertEqual(self.user.license_number, form_data["license_number"])
        self.assertEqual(response.status_code, 302)

    def test_delete_driver(self):
        count = get_user_model().objects.count()
        url = reverse("taxi:driver-delete", kwargs={"pk": self.user1.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.count() + 1, count)

    def test_search_driver(self):
        form_data = {"username": "test_admin"}
        response = self.client.get(self.drivers_list_url, data=form_data)
        driver = get_user_model().objects.all().filter(
            username=form_data["username"]
        )

        self.assertEqual(len(response.context["driver_list"]), len(driver))
        self.assertEqual(list(response.context["driver_list"]), list(driver))
        self.assertTemplateUsed(response, "taxi/driver_list.html")
