from django.db import models

__all__ = (
    'Ingredient',
)


class Ingredient(models.Model):
    # 이름
    name = models.CharField(max_length=30)
    # 설명
    description = models.TextField(max_length=256)
    # 작성자
    # user = models.ForeignKey(PickyUser)
    # 단위
    unit = models.CharField(max_length=30)
    # 칼로리
    cal = models.PositiveIntegerField(default=0)
