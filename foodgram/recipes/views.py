from django.http import Http404
from django.db.models import Q
from django.views.generic import CreateView, ListView

from .models import Recipe
from .utils import CachedPaginator


class Index(ListView):
    queryset = Recipe.objects.select_related('author')
    context_object_name = 'recipes'
    template_name = 'recipes/indexNotAuth.html'
    paginator_class = CachedPaginator
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        tags = self.get_tags()

        query_q = Q()
        for tag, checked in tags.items():
            if checked:
                query_q |= Q(**{"tags__contains": tag})
        if query_q:
            self.object_list = self.get_queryset().filter(query_q)
        else:
            self.object_list = Recipe.objects.none()

        context = self.get_context_data()
        context.update(tags)
        return self.render_to_response(context)

    def get_tags(self):
        tags = {}
        query_params = self.request.GET
        for tag_name, _ in Recipe.tags.field.choices:
            if tag_name not in query_params:
                tags[tag_name] = True
            elif query_params[tag_name] == 'no':
                tags[tag_name] = False
            else:
                raise Http404(f'Invalid value of the parameter "{tag_name}"')
        return tags


class CreateRecipeView(CreateView):
    model = Recipe
    fields = ('title', 'text', 'ingredients', 'tags', 'time_for_preparing')
    template_name = 'recipes/formRecipe.html'
