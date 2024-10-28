import freezegun
from rest_framework import status
from user.models import User, Follower
from post.models import Post, Like

from datetime import datetime, timedelta

from rest_framework.test import APITestCase


class PostTests(APITestCase):
    def setUp(self):
        """
        Creates user data for login, stores user data for its creation, creates one user and saves this user
        autentication credentials
        """
        self.user_data_for_login = dict(
            username="testuser",
            password="testpass",
        )
        self.data = dict(
            email="foo@bar.com", name="Foo Bar", **self.user_data_for_login
        )

        self.user = User.objects.create_user(**self.data)

        self._response = self.client.post(
            path="/api/token/", data=self.user_data_for_login
        )
        self.auth = {
            "HTTP_AUTHORIZATION": f"Bearer {self._response.data['access']}",
        }

    def test_post_create_1(self):
        """
        Given:
          - one user
          - the data to create one post
        When:
          - the request for create post is done `POST /api/posts/`
        Then:
          - the status code returned must be HTTP_201_CREATED
          - the response must have the text content equal to the created one
        """
        data_post = {"text": "Hello mini twitter!"}

        self.assertEqual(Post.objects.count(), 0)
        response = self.client.post(path=f"/api/posts/", data=data_post, **self.auth)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Post.objects.count(), 1)

        p = Post.objects.get(id=response.data["id"])
        self.assertEqual(p.text, data_post["text"])
        self.assertEqual(response.data["text"], data_post["text"])

    def test_post_create_2(self):
        """
        Given:
          - one user
          - the data to create one post with one image
        When:
          - the request for create post is done `POST /api/posts/` with format="multipart"
        Then:
          - the status code returned must be HTTP_201_CREATED
          - the response must have the text content equal to the created one
          - the base path '/images/image_' must be in the response.data["image"] field
        """

        data_post = {
            "text": "Hello mini twitter!",
            "image": open("post/test_utils/image.jpeg", "rb"),
        }

        self.assertEqual(Post.objects.count(), 0)
        response = self.client.post(
            path=f"/api/posts/", data=data_post, format="multipart", **self.auth
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Post.objects.count(), 1)

        p = Post.objects.get(id=response.data["id"])
        self.assertEqual(p.text, data_post["text"])
        self.assertEqual(response.data["text"], data_post["text"])
        self.assertIn("/images/image_", response.data["image"], response.data)

    def test_post_delete(self):
        """
        Given:
          - one user
          - the data to create one post
          - the post is created
        When:
          - the request for create user is done `DELETE /api/posts/{p.id}/delete/`
        Then:
          - the status code returned must be HTTP_204_NO_CONTENT
          - must not exist Post entries
        """
        data_post = {"text": "Some text. Simple twitter!"}

        self.assertEqual(Post.objects.count(), 0)
        response = self.client.post(path=f"/api/posts/", data=data_post, **self.auth)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Post.objects.count(), 1)

        p = Post.objects.get(user=self.user)
        self.assertEqual(p.user, self.user)
        self.assertEqual(p.text, data_post["text"])

        response2 = self.client.delete(path=f"/api/posts/{p.id}/delete/", **self.auth)

        self.assertEqual(response2.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_post_edit(self):
        """
        Given:
          - one user
          - the data to create one post, data_post
          - the post is created
          - the data to an edited post, edited_data_post
        When:
          - the request for create user is done `PATCH /api/posts/{p.id}/edit/`
        Then:
          - the status code returned must be HTTP_204_NO_CONTENT
          - the edited post must have its content equal to the data send to edit it
        """
        data_post = {"text": "Some twitter..."}

        self.assertEqual(Post.objects.count(), 0)
        response = self.client.post(path=f"/api/posts/", data=data_post, **self.auth)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Post.objects.count(), 1)

        p = Post.objects.get(id=response.data["id"])
        self.assertEqual(p.text, data_post["text"])

        edited_data_post = {"text": "a b c"}

        response2 = self.client.patch(
            path=f"/api/posts/{p.id}/edit/", data=edited_data_post, **self.auth
        )

        self.assertEqual(
            response2.status_code, status.HTTP_204_NO_CONTENT, response2.data
        )
        self.assertEqual(Post.objects.count(), 1)

        p = Post.objects.get(user=self.user)
        self.assertEqual(p.user, self.user)
        self.assertEqual(p.text, edited_data_post["text"])


class LikeTests(APITestCase):
    def setUp(self):
        """
        Creates two user data for login, user for its creation, creates one user and saves user auth credentials
        """
        self.user1_data_for_login = dict(
            username="testuser",
            password="testpass",
        )
        self.data1 = dict(
            email="foo@bar.com", name="Foo Bar", **self.user1_data_for_login
        )

        self.user1 = User.objects.create_user(**self.data1)

        self._response = self.client.post(
            path="/api/token/", data=self.user1_data_for_login
        )
        self.auth_as_user1 = {
            "HTTP_AUTHORIZATION": f"Bearer {self._response.data['access']}",
        }

        self.user2_data_for_login = dict(
            username="xyzuser",
            password="123456",
        )
        self.data2 = dict(
            email="xyz@gmail.com", name="X Y Z", **self.user2_data_for_login
        )

        self.user2 = User.objects.create_user(**self.data2)
        self._response2 = self.client.post(
            path="/api/token/", data=self.user2_data_for_login
        )
        self.auth_as_user2 = {
            "HTTP_AUTHORIZATION": f"Bearer {self._response2.data['access']}",
        }

    def test_like_create_1(self):
        """
        Note: the same user who posted it is the one who liked it.
        Given:
          - one user autenticated
          - one created post (a tweet)
        When:
          - the request for create user is done `POST /api/posts/{p.id}/like/`
            with the autenticated as user1
        Then:
          - the status code returned must be HTTP_201_CREATED
          - exist one Like entry in database
          - the user who liked is the user1
          - the post atribute from the created like is the created post
        """
        data_post = {"text": "AA BB CC"}

        self.assertEqual(Post.objects.count(), 0)
        response = self.client.post(
            path=f"/api/posts/", data=data_post, **self.auth_as_user1
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Post.objects.count(), 1)

        p = Post.objects.get(user=self.user1)
        self.assertEqual(p.text, data_post["text"])

        response2 = self.client.post(
            path=f"/api/posts/{p.id}/like/", **self.auth_as_user1
        )
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED, response2.data)
        self.assertEqual(Like.objects.count(), 1)

        like = Like.objects.get(user=self.user1, post=p)
        self.assertEqual(like.user, self.user1)
        self.assertEqual(like.post, p)

    def test_like_create_2(self):
        """
        Note: as it is implemented now, the same user can like many times the same post.
        Given:
          - one user
          - one created post (a tweet)
        When:
          - the request for create user is done `POST /api/posts/{p.id}/like/`
            with the autenticated as user1
        Then:
          - the status code returned must be HTTP_201_CREATED
          - exist one Like entry in database
        When:
          - the request for create user is done `POST /api/posts/{p.id}/like/`
        Then:
          - the status code returned must be HTTP_201_CREATED
          - exist two Like entries in database
        """
        data_post = {"text": "Bang!"}

        self.assertEqual(Post.objects.count(), 0)
        response = self.client.post(
            path=f"/api/posts/", data=data_post, **self.auth_as_user1
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Post.objects.count(), 1)

        p = Post.objects.get(user=self.user1)
        self.assertEqual(p.text, data_post["text"])

        response2 = self.client.post(
            path=f"/api/posts/{p.id}/like/", **self.auth_as_user1
        )
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED, response2.data)

        response3 = self.client.post(
            path=f"/api/posts/{p.id}/like/", **self.auth_as_user1
        )
        self.assertEqual(Like.objects.count(), 2)
        self.assertEqual(response3.status_code, status.HTTP_201_CREATED, response3.data)

    def test_like_create_3(self):
        """
        Given:
          - one user
          - one created post (a tweet)
        When:
          - the request for create user is done `POST /api/posts/{p.id}/like/`
            with the autenticated as user2
        Then:
          - the status code returned must be HTTP_201_CREATED
          - exist one Like entry in database
        """
        data_post = {"text": "Aeiou"}

        self.assertEqual(Post.objects.count(), 0)
        response = self.client.post(
            path=f"/api/posts/", data=data_post, **self.auth_as_user1
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Post.objects.count(), 1)

        p = Post.objects.get(user=self.user1)
        self.assertEqual(p.text, data_post["text"])

        response2 = self.client.post(
            path=f"/api/posts/{p.id}/like/", **self.auth_as_user2
        )
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED, response2.data)
        self.assertEqual(Like.objects.count(), 1)

        like = Like.objects.get(user=self.user2, post=p)
        self.assertEqual(like.user, self.user2)
        self.assertEqual(like.post, p)


class FeedTests(APITestCase):
    def setUp(self):
        """
        Creates two user data for login, stores two  user data for users creation, creates two users and saves
        the autentication credentials
        """
        # User one
        self.user_data_for_login1 = dict(
            username="testuser",
            password="testpass",
        )
        self.data1 = dict(
            email="foo@bar.com", name="Foo Bar", **self.user_data_for_login1
        )

        self.user1 = User.objects.create_user(**self.data1)

        self._response1 = self.client.post(
            path="/api/token/", data=self.user_data_for_login1
        )
        self.auth1 = {
            "HTTP_AUTHORIZATION": f"Bearer {self._response1.data['access']}",
        }

        # User two
        self.user_data_for_login2 = dict(
            username="testuser2",
            password="testpass",
        )
        self.data2 = dict(
            email="foo2@bar.com", name="Foo Bar", **self.user_data_for_login2
        )

        self.user2 = User.objects.create_user(**self.data2)
        self._response2 = self.client.post(
            path="/api/token/", data=self.user_data_for_login2
        )
        self.auth2 = {
            "HTTP_AUTHORIZATION": f"Bearer {self._response2.data['access']}",
        }

        # Creates the Follower entry
        Follower.objects.create(following=self.user2, follower=self.user1)

    def test_feed_1(self):
        """
        Given:
          - 2 tweets created by user2
          - user2 is followed by user1
        When:
          - the request for get feed is done `GET /api/feed/`
            with the autenticated as user1
        Then:
          - the status code returned must be HTTP_200_OK
          - the results list in response.data (the feed for user1) have 2 items
        When:
          - the request for get feed is done `GET /api/feed/`
            with the autenticated as user2
        Then:
          - the status code returned must be HTTP_200_OK
          - the results list in response.data (the feed for user2) have 2 items
        """
        data_post1 = {"text": "Some twitter..."}

        self.assertEqual(Post.objects.count(), 0)
        response = self.client.post(path=f"/api/posts/", data=data_post1, **self.auth2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Post.objects.count(), 1)

        data_post2 = {"text": "Foo bar..."}

        response = self.client.post(path=f"/api/posts/", data=data_post2, **self.auth2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Post.objects.count(), 2)

        self.assertEqual(Follower.objects.count(), 1)
        f = Follower.objects.get(following=self.user2, follower=self.user1)
        self.assertEqual(f.following, self.user2)
        self.assertEqual(f.follower, self.user1)

        response = self.client.get(path=f"/api/feed/", **self.auth1)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data["results"]), 2, response.data)

        response = self.client.get(path=f"/api/feed/", **self.auth2)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data["results"]), 2, response.data)

    def test_feed_2(self):
        """
        Given:
          - 2 tweets created by user1
          - user2 is followed by user1
        When:
          - the request for get feed is done `GET /api/feed/`
            with the autenticated as user1
        Then:
          - the status code returned must be HTTP_200_OK
          - the results list in response.data (the feed for user1) have 2 items
        When:
          - the request for get feed is done `GET /api/feed/`
            with the autenticated as user2
        Then:
          - the status code returned must be HTTP_200_OK
          - the results list in response.data (the feed for user2) have 2 items
        """
        data_post1 = {"text": "Some twitter..."}

        self.assertEqual(Post.objects.count(), 0)
        response = self.client.post(path=f"/api/posts/", data=data_post1, **self.auth1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Post.objects.count(), 1)

        data_post2 = {"text": "Foo bar..."}

        response = self.client.post(path=f"/api/posts/", data=data_post2, **self.auth1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Post.objects.count(), 2)

        self.assertEqual(Follower.objects.count(), 1)
        f = Follower.objects.get(following=self.user2, follower=self.user1)
        self.assertEqual(f.following, self.user2)
        self.assertEqual(f.follower, self.user1)

        response = self.client.get(path=f"/api/feed/", **self.auth1)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data["results"]), 2, response.data)

        response = self.client.get(path=f"/api/feed/", **self.auth2)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data["results"]), 2, response.data)

    def test_feed_cache(self):
        """
        Given:
          - 2 tweets created by user1
          - user2 is followed by user1
        When:
          - the request for get feed is done `GET /api/feed/`
            with the autenticated as user1
        Then:
          - the status code returned must be HTTP_200_OK
          - the results list in response.data (the feed for user1) have 2 items
        When:
          - has been passed 2 minutes (the cache time is 1minute)
          - the request for create user is done `GET /api/feed/`
        Then:
          - the status code returned must be HTTP_200_OK
          - the results list in response.data (the feed for user1) have 3 items
        """
        data_post1 = {"text": "Some twitter..."}

        self.assertEqual(Post.objects.count(), 0)
        response = self.client.post(path=f"/api/posts/", data=data_post1, **self.auth2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Post.objects.count(), 1)

        data_post2 = {"text": "Foo barr..."}

        response2 = self.client.post(path=f"/api/posts/", data=data_post2, **self.auth2)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED, response2.data)
        self.assertEqual(Post.objects.count(), 2)

        response = self.client.get(path=f"/api/feed/", **self.auth1)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data["results"]), 2, response.data)

        data_post3 = {"text": "Go go..."}
        response3 = self.client.post(path=f"/api/posts/", data=data_post3, **self.auth2)
        self.assertEqual(response3.status_code, status.HTTP_201_CREATED, response3.data)
        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get(path=f"/api/feed/", **self.auth1)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data["results"]), 2, response.data)

        later = datetime.now() + timedelta(minutes=2)
        with freezegun.freeze_time(later):
            response = self.client.get(path=f"/api/feed/", **self.auth1)
            self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
            self.assertEqual(len(response.data["results"]), 3, response.data)
