from django.db import models

from ingredient.models import Ingredient

__all__ = (
    'Recipe',
    'RecipeStep',
    'RecipeStepComment',
)


class Recipe(models.Model):
    """
    중간자 모델이 필요한 테이플은 주석
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    # user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    # like_users = models.ManyToManyField(User)
    like_count = models.PositiveIntegerField(default=0)
    bookmark_count = models.PositiveIntegerField(default=0)
    ingredient = models.ManyToManyField(
        Ingredient,
        related_name='Recipe_Ingredient',
        through='Recipe_Ingredient',
    )
    # tag = models.ManyToManyField(Tag)
    # rate = models.ManyToManyField(Rate)
    # bookmark = models.ManyToManyField(Bookmark)
    rate_sum = models.PositiveIntegerField(default=0)
    img_recipe = models.ImageField()
    cal_sum = models.PositiveIntegerField(default=0)

class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe)
    step = models.PositiveIntegerField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_timer = models.BooleanField(default=False)
    timer_timer = models.PositiveIntegerField(default=0)
    img_step = models.ImageField()

class RecipeReview(models.Model):
    recipe = models.ForeignKey(Recipe)
    # author = models.ForeignKey(User)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    img_review = models.ImageField()

class RecipeStepComment(models.Model):
    recipe_detail = models.ForeignKey(RecipeStep)
    # author = models.ForeignKey(User)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
