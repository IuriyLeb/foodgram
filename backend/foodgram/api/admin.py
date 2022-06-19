from django.contrib import admin
from .models import Tag, Recipe, Ingredient
from django.contrib.auth.models import User


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = (
        'name', 'slug', 'color'
    )


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
    )

    list_filter = ('name', 'author', 'tags')


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )

    list_filter = ('name', )


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name'
    )
    list_filter = ('email', 'username')


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Ingredient, IngredientAdmin)
