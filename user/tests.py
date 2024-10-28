from django.test import TestCase
from rest_framework import status
from .models import User, Follower


from rest_framework.test import APITestCase


class UserViewSetTestCase(TestCase):
    def setUp(self):
        """
        Creates helper data for tests, user data for login and two data sets for user creation
        """
        self.user_data_for_login = dict(
            username="foobar",
            password="123",
        )
        self.data1 = dict(
            email="foo@bar.com", name="Foo Bar", **self.user_data_for_login
        )

        self.data2 = dict(
            username="foobar2",
            email="foo@bar2.com",
            name="Foo2",
            password="5678",
        )

    def test_create_1(self):
        """
        Given:
          - a payload with valid data to create one user
          - does not exist users in database
        When:
          - the request for create user is done `POST /api/user/`
        Then:
          - the status code returned must be HTTP_201_CREATED
          - there must be one user in database
          - the user id must be in the response
          - the password must not be in the response
          - the other fields in the response must be equal to the ones sent
        """
        self.assertEqual(User.objects.count(), 0)

        response = self.client.post(path="/api/user/", data=self.data1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        self.assertEqual(User.objects.count(), 1)
        self.assertIn("id", response.data)

        result_data = response.data
        del result_data["id"]
        del result_data["password"]
        expect_data = self.data1
        del expect_data["password"]
        self.assertDictEqual(result_data, expect_data)

    def test_create_2(self):
        """
        Given:
          - a payload with invalid data to create one user,
            in this case any field that is sent to API as empt or as space.
        When:
          - the request for create user is done `POST /api/user/`
        Then:
          - the status code returned must be HTTP_400_BAD_REQUEST
        """
        for key in self.data1.keys():
            data = self.data1

            data[key] = ""
            response = self.client.post(path="/api/user/", data=data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

            data[key] = " "
            response = self.client.post(path="/api/user/", data=data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_3(self):
        """
        Given:
          - a payload with invalid data to create one user,
            in this case any field missing.
        When:
          - the request for create user is done `POST /api/user/`
        Then:
          - the status code returned must be HTTP_400_BAD_REQUEST
        """
        for key in self.data1.keys():
            data = dict(self.data1)

            del data[key]
            response = self.client.post(path="/api/user/", data=data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_followers_1(self):
        """
        Given:
          - given two users user1 and user2 and that user2 follows user1
        When:
          - the request for `/api/user/{user1.id}/followers/`
        Then:
          - the status code returned must be HTTP_200_OK
          - the user id must be in the response
          - the other fields in the response must be equal to the ones sent
        """
        user1 = User.objects.create_user(**self.data1)
        user2 = User.objects.create_user(**self.data2)

        Follower.objects.create(following=user1, follower=user2)

        response = self.client.post(path="/api/token/", data=self.user_data_for_login)
        auth = {
            "HTTP_AUTHORIZATION": f"Bearer {response.data['access']}",
        }

        response2 = self.client.get(path=f"/api/user/{user1.id}/followers/", **auth)
        self.assertEqual(response2.status_code, status.HTTP_200_OK, response2.data)

        result_data = response2.data
        for result in result_data["results"]:
            self.assertIn("id", result)
            del result["id"]

        expected_data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [{"username": "foobar2", "name": "Foo2"}],
        }
        self.assertDictEqual(result_data, expected_data)

    def test_follow_1(self):
        """
        Given:
          - given two users user1 and user2
          - does not exist Follower in database
        When:
          - the request for `/api/user/{user2.id}/follow/`
        Then:
          - the status code returned must be HTTP_204_NO_CONTENT
          - exist one Follower entry in database
        """
        user1 = User.objects.create_user(**self.data1)
        user2 = User.objects.create_user(**self.data2)

        response_auth = self.client.post(
            path="/api/token/", data=self.user_data_for_login
        )
        auth = {
            "HTTP_AUTHORIZATION": f"Bearer {response_auth.data['access']}",
        }

        self.assertEqual(Follower.objects.count(), 0)
        response_follow = self.client.patch(
            path=f"/api/user/{user2.id}/follow/", **auth
        )

        self.assertEqual(
            response_follow.status_code,
            status.HTTP_204_NO_CONTENT,
            response_follow.data,
        )
        self.assertEqual(Follower.objects.count(), 1)

        f1 = Follower.objects.get(follower=user1)
        f2 = Follower.objects.get(following=user2)

        self.assertEqual(f1.following, user2)
        self.assertEqual(f1.follower, user1)

        self.assertEqual(f2.following, user2)
        self.assertEqual(f2.follower, user1)

    def test_unfollow_1(self):
        """
        Given:
          - given two users user1 and user2 and that user2 follows user1
          - exists the Follower entry from user1 and user2
        When:
          - the request for `PATCH /api/user/{user2.id}/unfollow/`
        Then:
          - the status code returned must be HTTP_204_NO_CONTENT
          - does not exist Follower entry in database
        """
        user1 = User.objects.create_user(**self.data1)
        user2 = User.objects.create_user(**self.data2)

        Follower.objects.create(following=user2, follower=user1)
        self.assertEqual(Follower.objects.count(), 1)

        response = self.client.post(path='/api/token/', data=self.user_data_for_login)
        auth = {
            "HTTP_AUTHORIZATION": f"Bearer {response.data['access']}",
        }

        response2 = self.client.get(path=f"/api/user/{user2.id}/followers/", **auth)
        self.assertEqual(response2.status_code, status.HTTP_200_OK, response2.data)

        self.assertEqual(response2.data["results"][0]["username"], user1.username)

        response3 = self.client.patch(path=f"/api/user/{user2.id}/unfollow/", **auth)

        self.assertEqual(
            response3.status_code, status.HTTP_204_NO_CONTENT, response3.data
        )
        self.assertEqual(Follower.objects.count(), 0)


class AuthTests(APITestCase):
    def setUp(self):
        """
        Creates user data for user login and user creation, and creates one user
        """
        self.user_data_for_login = dict(
            username="testuser",
            password="testpass123",
        )
        self.data = dict(
            email="foo@bar.com", name="Foo Bar", **self.user_data_for_login
        )
        self.user = User.objects.create_user(**self.data)

    def test_obtain_token(self):
        """
        Given:
          - given one user
          - the user login data
        When:
          - the request for `POST /api/token/` is done
        Then:
          - the status code returned must be HTTP_200_OK
          - the user access must be in the response
          - the user refresh must be in the response
        """
        self.assertEqual(1, User.objects.count())
        self.assertEqual(self.user, User.objects.get())

        response = self.client.post("/api/token/", self.user_data_for_login)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_refresh_token(self):
        """
        Given:
          - one user
          - the user login data
        When:
          - the request for `POST /api/token/` is done
        Then:
          - the status code returned must be HTTP_200_OK
          - the response must have, in side data, the refresh key
        When:
          - the request for `POST /api/token/refresh/` is done
        Then:
          - the status code returned must be HTTP_200_OK
          - the response must have, in side data, the access key
        """
        self.assertEqual(1, User.objects.count())
        self.assertEqual(self.user, User.objects.get())

        # First, obtain a token
        response = self.client.post("/api/token/", self.user_data_for_login)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        refresh = response.data["refresh"]

        # Now, refresh the token
        response = self.client.post("/api/token/refresh/", {"refresh": refresh})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_obtain_token_invalid_credentials(self):
        """
        Given:
          - a valid username but a wrong password
        When:
          - the request for `POST /api/token/` is done
        Then:
          - the status code returned must be HTTP_401_UNAUTHORIZED
        """
        data = dict(self.user_data_for_login)
        data["password"] = "wrongpassword"

        response = self.client.post("/api/token/", data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_invalid(self):
        """
        Given:
          - an invalid refresh token
        When:
          - the request for `POST /api/token/refresh/` is done
        Then:
          - the status code returned must be HTTP_401_UNAUTHORIZED
        """
        data = {"refresh": "invalidtoken"}
        response = self.client.post("/api/token/refresh/", data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
