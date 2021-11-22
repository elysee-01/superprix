from django.db import models


class Client(models.Model):
    """
    Clients models
    """

    client = models.CharField(max_length=255)
    achats = models.ManyToManyField("mainapp.Produit", related_name="client_products")

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.client


class Produit(models.Model):
    """
    Products models
    """

    produit = models.CharField(max_length=255, help_text="Nom du produit")
    prix = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"

    def __str__(self):
        return self.produit
