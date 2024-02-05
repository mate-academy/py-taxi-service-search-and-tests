from django.test import TestCase
from django.urls import reverse


class AccessTest(TestCase):
    """
    Test case for checking access control on various views in the taxi app.
    """

    def setUp(self):
        """
        Set up the necessary data for the test case.
        """
        self.urls = [
            reverse("taxi:manufacturer-list"),
            reverse("taxi:manufacturer-create"),
            reverse("taxi:car-list"),
            reverse("taxi:car-create"),
            reverse("taxi:car-detail", kwargs={"pk": 1}),
            reverse("taxi:driver-list"),
            reverse("taxi:driver-create"),
            reverse("taxi:driver-detail", kwargs={"pk": 1}),
        ]

    def test_login_required_mixin(self):
        """
        Test the LoginRequiredMixin for restricted access to views.

        This method iterates through the list of URLs and checks that
        attempting to access each URLwithout being logged in results in a
        status code other than 200.
        """
        for url in self.urls:
            self.assertNotEqual(self.client.get(url).status_code, 200)
