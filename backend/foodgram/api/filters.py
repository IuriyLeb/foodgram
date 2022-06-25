import django_filters
from django_filters import FilterSet

from recipes.models import Recipe, Tag


class RecipeFilterSet(FilterSet):
    """
    Filter for RecipeViewSet.
    """
    author = django_filters.NumberFilter(field_name='author__id')
    tags = django_filters.ModelMultipleChoiceFilter(field_name='tags__slug',
                                                    to_field_name='slug',
                                                    queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = ['author', 'tags']
