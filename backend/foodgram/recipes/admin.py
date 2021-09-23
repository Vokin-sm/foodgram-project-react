from django.contrib import admin

from .models import Favorites, Recipe, ShoppingList


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'author',
        'get_count_in_favorites',
    )
    search_fields = ('name',)
    list_filter = ('name', 'author', 'tags')
    empty_value_display = '-пусто-'

    def get_count_in_favorites(self, obj):
        return len(Favorites.objects.filter(recipe=obj))

    get_count_in_favorites.short_description = 'количество в избранном'


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'recipe')
    search_fields = ('author',)
    list_filter = ('author',)


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'recipe')
    search_fields = ('author',)
    list_filter = ('author',)
