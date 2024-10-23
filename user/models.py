import uuid

from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(verbose_name="username", max_length=20, unique=True, validators=[UnicodeUsernameValidator])
    email = models.EmailField(verbose_name="endereço de email", unique=True)
    name = models.CharField(verbose_name="nome do usuário", max_length=200)
    password = models.CharField(verbose_name="senha do usuário", max_length=150)

    is_staff = models.BooleanField("É funcionário?", default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return f"Usuário ({self.username})"


# class Follower(BaseModel):
#     following = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name="followings")
#     follower = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name="followers")
#
#     class Meta:
#         unique_together = (('following', 'follower'),)
#         ordering = ["-created_at"]
#         verbose_name = "Seguidor"
#         verbose_name_plural = "Seguidores"
#
#     def __str__(self):
#         return f"{self.follower.username} segue {self.following.username}"
