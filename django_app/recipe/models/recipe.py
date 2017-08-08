from django.db import models

from ingredient.models import Ingredient
from member.models import PickyUser

__all__ = (
    'Recipe',
    'RecipeReview',
    'RecipeStepComment',
    'RecipeStep',
)


class Recipe(models.Model):
    """
    중간자 모델이 필요한 테이플은 주석
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(PickyUser)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    # like_users = models.ManyToManyField(User)
    like_count = models.PositiveIntegerField(default=0)
    bookmark_count = models.PositiveIntegerField(default=0)
    ingredient = models.ManyToManyField(
        Ingredient,
        related_name='RecipeIngredient',
        through='RecipeIngredient',
    )
    # tag = models.ManyToManyField(Tag)
    # rate = models.ManyToManyField(Rate)
    # bookmark = models.ManyToManyField(Bookmark)
    rate_sum = models.PositiveIntegerField(default=0)
    img_recipe = models.ImageField(blank=True)
    cal_sum = models.PositiveIntegerField(default=0)

# Recipe 후기 작성
class RecipeReview(models.Model):
    # 후기를 작성할 Recipe
    recipe = models.ForeignKey(Recipe)
    # 후기 작성자
    # author = models.ForeignKey(PickyUser)
    # 후기 내용
    content = models.TextField()
    # 후기 생성시간
    created = models.DateTimeField(auto_now_add=True)
    # 후기 수정시간
    modified = models.DateTimeField(auto_now=True)
    # 후기 이미지
    img_review = models.ImageField()


class RecipeStep(models.Model):
    # 레시피
    recipe = models.ForeignKey(Recipe, related_name='recipes', on_delete=models.CASCADE)
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

    class Meta:
        unique_together = (
            ('recipe', 'step'),
        )


class RecipeStepComment(models.Model):
    recipe_detail = models.ForeignKey(RecipeStep)
    # author = models.ForeignKey(PickyUser)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
