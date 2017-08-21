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


class PickyUserListView(ListView):
    model = PickyUser


