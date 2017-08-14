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
            step=str(instance.step).rjust(2, '0'),
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
    중간자 모델이 필요한 테이블은 주석처리
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(PickyUser)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(
        PickyUser,
        related_name='recipe_user_set',
        through='RecipeLike',
    )
    like_count = models.PositiveIntegerField(default=0)
    bookmark_count = models.PositiveIntegerField(default=0)
    ingredient = models.ManyToManyField(
        Ingredient,
        related_name='RecipeIngredient',
        through='RecipeIngredient',
    )
    # tag = models.ManyToManyField(Tag)
    # rate = models.ManyToManyField(Rate)
    bookmarks = models.ManyToManyField(
        PickyUser,
        related_name='bookmark_user_set',
        through='BookMark',
    )
    rate_sum = models.FloatField(default=0)
    img_recipe = models.ImageField(
        upload_to=recipe_img_directory,
        # upload_to='recipe/',
        blank=True
    )
    cal_sum = models.PositiveIntegerField(default=0)

    # def like_counts(self):
    #     self.like_count = self.recipelike_set.count()
    #     # return self.like_count


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
    image_step = models.ImageField(upload_to=recipe_step_img_directory, blank=True)

    # step 숫자 자동입력 8/10 joe
    def save(self, *args, **kwargs):
        # 현재 레시피로 레시피스텝에 넣을 번호를 생성
        step = get_recipe_step_no(self.recipe)
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
    content = models.TextField(max_length=256)
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
    rate = models.FloatField(default=0)

    class Meta:
        unique_together = (
            ('user', 'recipe'),
        )

