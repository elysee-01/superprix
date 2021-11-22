from django.urls import path
from . import api

urlpatterns = [
    path("montant_plus_eleve/", api.ClientMontantPlusEleve.as_view()),
    path("prix_vente/<str:id>/", api.PrixDeVente.as_view()),
    path("add-client/", api.AddClient.as_view()),
]
