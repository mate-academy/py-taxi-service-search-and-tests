from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class PublicDriverTest(TestCase):
    def setUp(self):
        self.driver = get_user_model().objects.create_user(
            username="Test Driver",
            password="TestPassword123",
        )
        self.driver.save()

        self.url_list = [
            reverse("taxi:driver-list"),
            reverse(
                "taxi:driver-detail",
                kwargs={"pk": self.driver.id}
            ),
            reverse("taxi:driver-create"),
            reverse(
                "taxi:driver-update",
                kwargs={"pk": self.driver.id}
            ),
            reverse(
                "taxi:driver-delete",
                kwargs={"pk": self.driver.id}
            )
        ]

    def test_login_required(self):
        response_list = [self.client.get(url) for url in self.url_list]
        for res in response_list:
            self.assertNotEqual(res.status_code, 200)


class PrivateDriverTest(TestCase):
    def setUp(self):
        self.driver1 = get_user_model().objects.create_user(
            username="TestDriver",
            first_name="Test First",
            last_name="Test Last",
            password="TestPassword123",
            license_number="ABC12345",
        )
        self.driver1.save()

        self.driver2 = get_user_model().objects.create_user(
            username="OtherDriver",
            password="TestPassword456",
            license_number="NFS12345",
        )
        self.driver2.save()

        self.client.force_login(self.driver1)

        self.url_list = [
            reverse("taxi:driver-list"),
            reverse(
                "taxi:driver-detail",
                kwargs={"pk": self.driver1.id}
            ),
            reverse("taxi:driver-create"),
            reverse(
                "taxi:driver-update",
                kwargs={"pk": self.driver1.id}
            ),
            reverse(
                "taxi:driver-delete",
                kwargs={"pk": self.driver1.id}
            )
        ]

        self.response_list = [self.client.get(url) for url in self.url_list]

        self.templates_list = [
            "taxi/driver_list.html",
            "taxi/driver_detail.html",
            "taxi/driver_form.html",
            "taxi/driver_form.html",
            "taxi/driver_confirm_delete.html"
        ]

        self.driver_list_url = reverse("taxi:driver-list")
        self.driver_list_response = self.client.get(self.driver_list_url)

    def test_user_logged_in_required(self):
        for res in self.response_list:
            self.assertEqual(res.status_code, 200)

    def test_display_all_drivers(self):
        drivers = get_user_model().objects.all()
        self.assertEqual(
            list(self.driver_list_response.context["driver_list"]),
            list(drivers)
        )

    def test_search_drivers(self):
        search_driver = get_user_model().objects.filter(
            username__icontains="Test"
        )
        search_driver_response = self.client.get(
            self.driver_list_url + "?username=Test"
        )
        self.assertEqual(
            list(search_driver),
            list(search_driver_response.context["driver_list"])
        )

    def test_correct_templates(self):
        for num in range(len(self.templates_list)):
            self.assertTemplateUsed(
                self.response_list[num],
                self.templates_list[num]
            )
