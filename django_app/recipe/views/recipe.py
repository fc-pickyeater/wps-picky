from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, FormView
from django.views.generic.edit import ModelFormMixin

from recipe.forms import RecipeCreateForm, RecipeStepCreateForm
from recipe.models import Recipe, RecipeStep


class RecipeDetailView(DetailView):
    model = Recipe


class RecipeListView(ListView):
    model = Recipe


# class RecipeListView2(FormView):
#     pass


class RecipeCreateView(ModelFormMixin, FormView):
    form_class = RecipeCreateForm
    formset_class = inlineformset_factory(
            parent_model=Recipe,
            model=RecipeStep,
            form=RecipeStepCreateForm,
            extra=1,
            can_order=True,
            can_delete=True,
    )
    object = None
    template_name = 'recipe/recipe_create2.html'
    success_url = reverse_lazy('recipe:recipestep_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'formset' not in kwargs:
            context['formset'] = self.get_formset
        return context

    def get_formset(self, **kwargs):
        kwargs.update(instance=self.object)
        return self.formset_class(**kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        formset = self.get_formset(data=self.request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_formset_valid(form, formset)
        else:
            return self.form_formset_invalid(form, formset)

    def form_formset_valid(self, form, formset):
        form.instance = self.get_form()
        form.instance = self.request.user
        formset.instance = self.get_formset(data=self.request.POST)
        formset.instance.recipe = form.instance

        form.save()
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_formset_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))



# class RecipeCreateView(CreateView):
#     model = Recipe
#     success_url = reverse_lazy('recipe:recipestep_create')
#     # form_class = RecipeCreateForm
#     # form_class = RecipeFormSet
#
#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.user = self.request.user
#         self.object.save()
#         # 임시로 레시피 리스트로 이동
#         return redirect('recipe:recipe_list')



