from django.db import models

from recipe.models import Recipe


class RecipeStep(models.Model):
    # 레시피
    recipe = models.ForeignKey(Recipe)
    # 단계
    step = models.PositiveIntegerField(default=0)
    # 설명
    description = models.TextField(max_length=256)
    # 생성시간
    created_date = models.DateTimeField(auto_now_add=True)
    # 수정시간
    modified_date = models.DateTimeField(auto_now=True)
    # 타이머 필요
    is_timer = models.BooleanField(default=False)
    # 조리시간
    timer = models.PositiveIntegerField(default=0)
    # 사진
    image_step = models.ImageField(blank=True)

