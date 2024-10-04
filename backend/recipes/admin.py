from django.contrib import admin

from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingList,
    Tag
)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Класс настройки модели Tag в админке."""

    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Класс настройки модели Ingridient в админке."""

    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Класс настройки модели Recipe в админке."""

    inlines = [IngredientInline]
    fields = ('tags', 'image', 'name', 'text', 'cooking_time', 'author')
    list_display = ('id',
                    'name',
                    'author',
                    'short_url_code',
                    'count_favorites')
    search_fields = ('name', 'author__username')
    list_filter = ('tags',)

    @admin.display(description='Добавлений в избранное:')
    def count_favorites(self, obj):
        return obj.favorite.count()


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """Класс настройки модели Recipe в админке."""

    list_display = ('recipe', 'ingredient', 'amount')
    search_fields = ('recipe__name', 'ingredient__username')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Класс настройки модели Favorite в админке."""
    list_display = ('pk', 'user')


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    """Класс настройки модели ShoppingList в админке."""
    list_display = ('pk', 'user', 'recipe')
