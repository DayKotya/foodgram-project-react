from django.contrib import admin

from recipes.models import (Tag,
                            Ingredient,
                            Recipe,
                            FavoriteRecipe,
                            ShoppingList,
                            RecipeIngredient)


class RecipeIngredientInLine(admin.TabularInline):
    model = RecipeIngredient


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_filter = ('name', )
    search_fields = ('name', )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInLine,)
    list_display = (
        'pk',
        'author',
        'name',
        'get_favorite_count'
    )
    readonly_fields = ('how_many_times_favorited',)
    list_filter = ('name', 'author', 'tags')

    def get_favorite_count(self, obj):
        return obj.favorite_recipes.count()

    @admin.display(description='Количество в избранных')
    def how_many_times_favorited(self, obj):
        return obj.favorite_recipes.count()

    get_favorite_count.short_description = 'Число добавлений в избранное'


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'user')


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount',)
    search_fields = (
        'recipe__name', 'recipe__author__username', 'recipe__author__email',)
    list_filter = ('recipe__tags',)


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'user')
