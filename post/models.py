from django.db import models

# Create your models here.

from common.models import BaseModel
from user.models import User

class Post(BaseModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="posts")
    text = models.CharField(verbose_name="Conteúdo do post", max_length=128)  # TODO: typo recreate
    image = models.ImageField(verbose_name="Imagem do post", upload_to="images", null=True, blank=True)


class Like(BaseModel):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="likes")
