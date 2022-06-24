from django.contrib import admin
from .models import Tag, Recipe, Ingredient, RecipeIngredient, Favorites, ShoppingCart


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug', 'color'
    )


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'in_favorited'
    )

    list_filter = ('tags',)
    search_fields = ('name', 'author', 'tags')

    def in_favorited(self, obj):
        return Favorites.objects.filter(
            recipe=obj
        ).count()


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )

    search_fields = ('name', )


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient'
    )


class FavoritesAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Favorites, FavoritesAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)

