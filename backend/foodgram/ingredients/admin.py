from django.contrib import admin

from .models import Component, Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
    )
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
        'amount',
    )
    search_fields = ('pk',)
