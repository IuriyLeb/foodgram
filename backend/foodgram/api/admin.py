from django.contrib import admin
from .models import Tag, Recipe, Ingredient


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author'
    )

    list_filter = ('name', 'author')


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )

    list_filter = ('name', )


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
