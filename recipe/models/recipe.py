from django.db import models

# Create your models here.

__all__ = (
    'Recipe',
    'RecipeDetail',
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
    # ingredient = models.ManyToManyField(Ingredient)
    # tag = models.ManyToManyField(Tag)
    # rate = models.ManyToManyField(Rate)
    # bookmark = models.ManyToManyField(Bookmark)
    rate_sum = models.PositiveIntegerField(default=0)
    img_recipe = models.ImageField()
    cal_sum = models.PositiveIntegerField(default=0)
