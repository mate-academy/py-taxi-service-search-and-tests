from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class ViewsTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="user.admin", password="testpassword12589"
        )
        self.client.force_login(self.admin_user)

        number_of_users = 6

        for users in range(number_of_users):
            get_user_model().objects.create(
                username="TestUser %s" % users,
                password="tests126 %s" % users,
                license_number="tes14856%s" % users,
            )

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get("/drivers/")
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, "taxi/driver_list.html")

    def test_pagination_is_five(self):
        resp = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"] == True)
        self.assertTrue(len(resp.context["driver_list"]) == 5)

    def test_lists_all_drivers(self):
        resp = self.client.get(reverse("taxi:driver-list") + "?page=2")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("is_paginated" in resp.context)
        self.assertTrue(resp.context["is_paginated"] == True)
        self.assertTrue(len(resp.context["driver_list"]) == 2)
