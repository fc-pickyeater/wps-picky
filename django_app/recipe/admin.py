from django.contrib import admin

from recipe.models import Recipe, RecipeReview, RecipeStep, RecipeStepComment

admin.site.register(Recipe)
admin.site.register(RecipeReview)
admin.site.register(RecipeStep)
admin.site.register(RecipeStepComment)

