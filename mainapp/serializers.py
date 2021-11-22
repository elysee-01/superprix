from rest_framework import serializers
from . import models


class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Produit
        fields = ("produit", "prix")


class ClientSerializer(serializers.ModelSerializer):
    achats = ProduitSerializer(many=True, required=False)

    class Meta:
        model = models.Client
        fields = ("id", "client", "achats")
