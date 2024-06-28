from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Advertisement


class UserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_register(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "password1": "12345",
                "password2": "12345",
                "email": "newuser@example.com",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "12345"}
        )
        self.assertEqual(response.status_code, 200)


class AdvertisementTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.ad = Advertisement.objects.create(
            title="Test Ad",
            advertiser_name="Test Advertiser",
            advertiser_link="http://example.com",
            publication_date="2024-01-01",
            submission_deadline="2024-01-10",
            bvpz_code="12345",
            purchase_type="Type1",
            advertisement_type="Type2",
        )

    def test_ad_list(self):
        response = self.client.get(reverse("ad_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Ad")
