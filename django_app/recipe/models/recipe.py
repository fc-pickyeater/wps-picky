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
    'BookMark',
    'RecipeLike',
    'RecipeRate',

    'Tag',
    'RecipeTag'
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
        date=instance.recipe.created_date.strftime('%Y-%m-%d'),
        title=instance.recipe.title,
        user=instance.recipe.user.pk,
    )
    recipe_step_img_filename = u'{step}-{title}-{microsecond}{extension}'.format(
        step=str(instance.step).rjust(2, '0'),
        title=instance.recipe.title,
        microsecond=datetime.datetime.now().microsecond,
        extension=os.path.splitext(filename)[1],
    )
    return 'recipe/{path}/{filename}'.format(
        path=recipe_img_path,
        filename=recipe_step_img_filename,
    )


# 레시피 후기 사진이 저장되는 경로와 파일 이름을 바꿔주는 함수
def recipe_review_img_directory(instance, filename):
    recipe_img_path = u'{date}-{title}-{user}'.format(
        date=instance.recipe.created_date.strftime('%Y-%m-%d'),
        title=instance.recipe.title,
        user=instance.recipe.user.pk,
    )
    recipe_review_img_filename = u'review-{title}-{microsecond}{extension}'.format(
        title=instance.recipe.title,
        microsecond=datetime.datetime.now().microsecond,
        extension=os.path.splitext(filename)[1],
    )
    return 'recipe/{path}/{filename}'.format(
        path=recipe_img_path,
        filename=recipe_review_img_filename,
    )


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(PickyUser)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        PickyUser,
        related_name='recipe_user_set',
        through='RecipeLike',
    )
    like_count = models.PositiveIntegerField(default=0)
    bookmark_count = models.PositiveIntegerField(default=0)
    # ingredient = models.ManyToManyField(
    #     Ingredient,
    #     related_name='RecipeIngredient',
    #     through='RecipeIngredient',
    # )
    ingredient = models.TextField(null=True)
    tag = models.ManyToManyField(
        'Tag',
        through='RecipeTag',
        related_name='RecipeTag',
    )
    bookmarks = models.ManyToManyField(
        PickyUser,
        related_name='bookmark_user_set',
        through='BookMark',
    )
    rate_sum = models.FloatField(default=0)
    img_recipe = models.ImageField(
        upload_to=recipe_img_directory,
        blank=True
    )
    cal_sum = models.PositiveIntegerField(default=0)


# 레시피 후기
class RecipeReview(models.Model):
    recipe = models.ForeignKey(
            Recipe,
            related_name='reviews',
            on_delete=models.CASCADE
    )
    user = models.ForeignKey(PickyUser)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    img_review = models.ImageField(
        upload_to=recipe_review_img_directory,
        blank=True,
    )


# 레시피 스텝
class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='recipes', on_delete=models.CASCADE)
    step = models.PositiveIntegerField(default=1)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_timer = models.BooleanField(default=False)
    timer = models.PositiveIntegerField(default=0)
    img_step = models.ImageField(upload_to=recipe_step_img_directory, blank=True)

    class Meta:
        ordering = ['recipe', 'step']

    # step 숫자 자동입력 8/10 joe
    def save(self, *args, **kwargs):
        # 현재 레시피로 레시피스텝에 넣을 번호를 생성
        if self.created_date is None:
            step = get_recipe_step_no(self.recipe)
        else:
            step = self.step
        # step 필드에 위 번호를 넣어준다.
        self.step = step
        super(RecipeStep, self).save(*args, **kwargs)


# 레시피 스텝에 넣을 번호를 정해주는 함수 8/10 joe
def get_recipe_step_no(recipe):
    # 현재 레시피스텝에 있는 스텝번호를 리스트로 가져와 내림차순으로 정렬
    cur_step = RecipeStep.objects.filter(recipe=recipe).order_by('-step').values_list('step', flat=True)
    # 리스트 값이 있으면 가장 처음 값에 1을 더해 리턴
    if cur_step:
        return cur_step[0] + 1
    # 리스트 값이 없으면 1을 리턴
    else:
        return 1


class RecipeStepComment(models.Model):
    recipe_step = models.ForeignKey(RecipeStep, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(PickyUser)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)


class BookMark(models.Model):
    recipe = models.ForeignKey(Recipe)
    user = models.ForeignKey(PickyUser)
    created_date = models.DateTimeField(auto_now_add=True)
    memo = models.TextField(max_length=256)

    class Meta:
        unique_together = (
            ('user', 'recipe'),
        )


class RecipeLike(models.Model):
    recipe = models.ForeignKey(Recipe)
    user = models.ForeignKey(PickyUser)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('user', 'recipe'),
        )


class RecipeRate(models.Model):
    recipe = models.ForeignKey(Recipe)
    user = models.ForeignKey(PickyUser)
    # 소수점 사용을 위한 필드 - hong 8/15
    rate = models.DecimalField(default=0, max_digits=3, decimal_places=1)

    class Meta:
        unique_together = (
            ('user', 'recipe'),
        )


# 일단 여기 써봄... 8/14 joe -> migrate 성공 8/14 joe
class Tag(models.Model):
    content = models.CharField(max_length=20, unique=True)
    url = models.CharField(max_length=200)


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag)
    created = models.DateTimeField(auto_now_add=True)
