from . import models
from . import serializers
from rest_framework import status
from rest_framework.views import APIView
from django.db.models.aggregates import Max, Sum
from rest_framework.response import Response


class PrixDeVente(APIView):

    def get(self, request, id, format=None):
        if not str(id).isdigit() or int(id) < 1:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        client = models.Client.objects.filter(id=id).first()
        if not client:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        article_prix_plus_eleve = client.achats.all().aggregate(prix_max=Max('prix')).get('prix_max')
        
        prixvente = client.achats.all().aggregate(prixvente=Sum('prix')).get('prixvente')
        
        if prixvente > 10000:
            # Reduction de 7% sur l'article ayant le prix le plus eleve
            prixvente = prixvente - (article_prix_plus_eleve * 0.07)
    
        data = {
            "prix_de_vente": prixvente
        }
        return Response(data)


class ClientMontantPlusEleve(APIView):

    def get(self, request, format=None):
        data = {}
        clients = models.Client.objects.values('id').annotate(total=Sum('achats__prix')).order_by('-total')
        if clients:
            _data = models.Client.objects.get(pk=clients[0].get('id'))
            data = serializers.ClientSerializer(_data).data
        return Response(data)
