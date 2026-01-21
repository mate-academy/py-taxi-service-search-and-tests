from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123"
        )
        self.client.force_login(self.admin_user)

        self.author = get_user_model().objects.create_user(
            username="test_author",
            password="<PASSWORD>",
        )


    def test_additional_info(self):
        self.author.first_name = "<FIRST NAME>"
        self.author.last_name = "<LAST NAME>"
        self.author.license_number = "AAA88887"
        self.author.save()

        url = reverse("admin:taxi_driver_change")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.author.first_name)
        self.assertContains(res, self.author.last_name)
        self.assertContains(res, self.author.license_number)

    def test_additional_info_listed(self):
        self.author.first_name = "<FIRST NAME>"
        self.author.last_name = "<LAST NAME>"
        self.author.license_number = "AAA88888"
        self.author.save()

        url = reverse(
            "admin:taxi_driver_changelist",
            args=[self.author.id]
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.author.first_name)
        self.assertContains(res, self.author.last_name)
        self.assertContains(res, self.author.license_number)
