import datetime
import os

from django.db import models

from ingredient.models import Ingredient
from member.models import PickyUser

__all__ = (
    'Recipe',
    'RecipeReview',
    'RecipeStepComment',
    'RecipeStep',
)


# 레시피 사진이 저장되는 경로와 파일 이름을 바꿔주는 함수
def recipe_img_directory(instance, filename):
    recipe_img_path = u'{date}-{title}-{user}'.format(
        date=datetime.datetime.now().strftime('%Y-%m-%d'),
        title=instance.title,
        user=instance.user.pk,
    )
    recipe_img_filename = u'00-{title}-{microsecond}{extension}'.format(
        title=instance.title,
        microsecond=datetime.datetime.now().microsecond,
        extension=os.path.splitext(filename)[1],
    )
    return 'recipe/{path}/{filename}'.format(
        path=recipe_img_path,
        filename=recipe_img_filename,
    )


# 레시피 스텝 사진이 저장되는 경로와 파일 이름을 바꿔주는 함수
def recipe_step_img_directory(instance, filename):
    recipe_img_path = u'{date}-{title}-{user}'.format(
        date=datetime.datetime.now().strftime('%Y-%m-%d'),
        title=instance.recipe.title,
        user=instance.recipe.user.pk,
    )
    recipe_step_img_filename = u'{step}-{title}-{microsecond}{extension}'.format(
        step=str(instance.step).rjust(2, 'd'),
        title=instance.recipe.title,
        microsecond=datetime.datetime.now().microsecond,
        extension=os.path.splitext(filename)[1],
    )
    return 'recipe/{path}/{filename}'.format(
        path=recipe_img_path,
        filename=recipe_step_img_filename,
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
    # like_users = models.ManyToManyField(PickyUser)
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
    img_recipe = models.ImageField(
        upload_to=recipe_img_directory,
        # upload_to='recipe/',
        blank=True
    )
    cal_sum = models.PositiveIntegerField(default=0)


class RecipeReview(models.Model):
    recipe = models.ForeignKey(Recipe)
    user = models.ForeignKey(PickyUser)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    img_review = models.ImageField()


class RecipeStep(models.Model):
    # 레시피
    recipe = models.ForeignKey(Recipe, related_name='recipes', on_delete=models.CASCADE)
    # 단계
    step = models.PositiveIntegerField(default=1)
    # 설명r
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
    image_step = models.ImageField(upload_to=recipe_step_img_directory, blank=True)

    class Meta:
        unique_together = (
            ('recipe', 'step'),
        )


class RecipeStepComment(models.Model):
    recipe_step = models.ForeignKey(RecipeStep, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(PickyUser)
    content = models.TextField(max_length=256)
    created_date = models.DateTimeField(auto_now_add=True)
    # update_date = models.DateTimeField(auto_now=True)
