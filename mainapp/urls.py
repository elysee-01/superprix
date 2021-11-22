from django.urls import path
from . import api

urlpatterns = [
    path("prix_plus_eleve/", api.ClientMontantPlusEleve.as_view()),
    path("prix_vente/<str:id>/", api.PrixDeVente.as_view()),
]
