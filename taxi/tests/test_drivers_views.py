from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DriverListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="password",
            license_number="AAA11111"
        )
        self.client.force_login(self.user)
        self.url = reverse("taxi:driver-list")

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_get_driver_list(self):
        get_user_model().objects.create_user(
            username="driver 2",
            password="password",
            license_number="ABC11111"
        )
        get_user_model().objects.create_user(
            username="driver 3",
            password="password",
            license_number="AAA11115"
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_list.html")
        self.assertEqual(
            list(get_user_model().objects.all()),
            list(response.context["object_list"]),
        )

    def test_search_driver_list(self):
        bob = get_user_model().objects.create_user(
            username="bob",
            password="password",
            license_number="ABC11111"
        )
        john = get_user_model().objects.create_user(
            username="john",
            password="password",
            license_number="AAA11115"
        )
        response = self.client.get(self.url, {"username": "bob"})
        self.assertIn(bob, response.context["object_list"])
        self.assertNotIn(john, response.context["object_list"])
        self.assertNotIn(self.user, response.context["object_list"])

    def test_search_empty_manufacturer_list(self):
        response = self.client.get(self.url, {"username": "bob"})
        self.assertEqual(0, len(response.context["object_list"]))


class DriverCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="password",
            license_number="AAA11111"
        )
        self.client.force_login(self.user)
        self.url = reverse("taxi:driver-create")

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_create_driver_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")

    def test_can_create_driver(self):
        response = self.client.post(
            self.url,
            data={
                "username": "bob",
                "license_number": "AAA11113",
                "first_name": "Bob",
                "last_name": "Smith",
                "password1": "1@Password!",
                "password2": "1@Password!",
            }
        )
        driver = get_user_model().objects.last()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("taxi:driver-detail", kwargs={"pk": driver.pk}),
        )
        self.assertEqual(2, get_user_model().objects.count())
        self.assertEqual(driver.username, "bob")
        self.assertEqual(driver.license_number, "AAA11113")

    def test_show_errors(self):
        response = self.client.post(
            self.url,
            data={
                "username": "driver",
                "license_number": "AAA111",
                "first_name": "",
                "last_name": "",
                "password1": "Password!",
                "password2": "Password!!",
            }
        )
        form = response.context["form"]
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            form,
            "username",
            "A user with that username already exists.",
        )
        self.assertFormError(
            form,
            "license_number",
            "License number should consist of 8 characters",
        )
        self.assertFormError(
            form,
            "password2",
            "The two password fields didn’t match.",
        )


class DriverLicenseUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="password",
            license_number="AAA11111"
        )
        self.client.force_login(self.user)
        self.url = reverse("taxi:driver-update", kwargs={"pk": self.user.pk})

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_update_driver_license_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_form.html")
        self.assertEqual(self.user, response.context["object"])

    def test_can_update_driver_license(self):
        response = self.client.post(
            self.url,
            data={"license_number": "ABC11111"}
        )
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("taxi:driver-list"))
        self.assertEqual("ABC11111", self.user.license_number)

    def test_show_errors(self):
        response = self.client.post(
            self.url,
            data={"license_number": ""}
        )
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFormError(form, "license_number", "This field is required.")


class DriverDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="password",
            license_number="AAA11111"
        )
        self.driver_to_delete = get_user_model().objects.create_user(
            username="driver to delete",
            password="password",
            license_number="AAA11112"
        )
        self.client.force_login(self.user)
        self.url = reverse(
            "taxi:driver-delete",
            kwargs={"pk": self.driver_to_delete.pk},
        )

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_delete_driver_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_confirm_delete.html")
        self.assertEqual(self.driver_to_delete, response.context["object"])

    def test_can_delete_driver(self):
        response = self.client.post(
            self.url,
        )
        pk = self.driver_to_delete.pk
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("taxi:driver-list"))
        self.assertFalse(get_user_model().objects.filter(id=pk).exists())


class DriverDetailViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="driver",
            password="password",
            license_number="AAA11111"
        )
        self.client.force_login(self.user)
        self.url = reverse("taxi:driver-detail", kwargs={"pk": self.user.pk})

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)

    def test_detail_driver_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "taxi/driver_detail.html")
        self.assertEqual(self.user, response.context["object"])
