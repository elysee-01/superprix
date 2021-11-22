from django.contrib import admin
from . import models


@admin.register(models.Client)
class Client(admin.ModelAdmin):
    list_display = ("client", )
    list_display_links = ["client"]
    search_fields = ("client",)

@admin.register(models.Produit)
class Produit(admin.ModelAdmin):
    list_display = ("produit", "prix", )
    list_display_links = ["produit", "prix"]
    search_fields = ("produit", )
