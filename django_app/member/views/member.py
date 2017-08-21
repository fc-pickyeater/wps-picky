from django.contrib.auth import get_user_model
from django.views.generic import DetailView, ListView
from django.views.generic.detail import SingleObjectMixin

from recipe.models import Recipe

PickyUser = get_user_model()

__all__ = (
    'PickyUserDetailView',
    'PickyUserListView',
)


class PickyUserDetailView(DetailView):
    model = PickyUser

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context['object'] = self.object
            context['recipe_list'] = Recipe.objects.filter(user=self.object)
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        context.update(kwargs)
        return super(SingleObjectMixin, self).get_context_data(**context)


class PickyUserListView(ListView):
    model = PickyUser


