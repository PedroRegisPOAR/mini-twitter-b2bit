from django.test import TestCase
from rest_framework import status
from user.models import User


from rest_framework.test import APITestCase



class PostTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_post_create(self):
        data = dict(
            username="testuser",
            password="testpass",
        )

        data_post = {
            "text": "dfnfdgjdsklrj"
        }

        response = self.client.post(path="/api/token/", data=data)
        auth = {
            "HTTP_AUTHORIZATION": f"Bearer {response.data['access']}",
        }

        response = self.client.post(path=f"/api/posts/", data=data_post, **auth)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        print(response.data)
