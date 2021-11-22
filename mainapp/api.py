from . import models
from . import serializers
from rest_framework import status
from rest_framework.views import APIView
from django.db.models.aggregates import Max, Sum
from rest_framework.response import Response
from .serializers import ClientSerializer
from rest_framework import generics


class PrixDeVente(APIView):
    """
    Retourne le prix de vente d'un utilisateur precis en appliqant
    la reduction si le montant total excede 10000F
    """

    def get(self, request, id, format=None):
        if not str(id).isdigit() or int(id) < 1:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        client = models.Client.objects.filter(id=id).first()
        if not client:
            return Response(status=status.HTTP_404_NOT_FOUND)

        article_prix_plus_eleve = (
            client.achats.all().aggregate(prix_max=Max("prix")).get("prix_max")
        )

        prixvente = (
            client.achats.all().aggregate(prixvente=Sum("prix")).get("prixvente")
        )

        if prixvente > 10000:
            # Reduction de 7% sur l'article ayant le prix le plus eleve
            prixvente = prixvente - (article_prix_plus_eleve * 0.07)

        data = {"prix_de_vente": prixvente}
        return Response(data)


class ClientMontantPlusEleve(APIView):
    """
    Retourne le client ayant le montant total
    le plus eleve sans la reduction
    """

    def get(self, request, format=None):
        data = {}
        clients = (
            models.Client.objects.values("id")
            .annotate(total=Sum("achats__prix"))
            .order_by("-total")
        )
        if clients:
            _data = models.Client.objects.get(pk=clients[0].get("id"))
            data = serializers.ClientSerializer(_data).data
        return Response(data)


class AddClient(generics.ListCreateAPIView):
    """
    Ajout d'un nouveau client selon le format:

    {
        "id": 1,
        "client": "James AKRAN",
        "achats": [
        {
            "produit": "Détergent OMO 1L",
            "prix": 1200
        },
        {
            "produit": "Huile Végétale AYA 90cl",
            "prix": 850
        },
        {
            "produit": "Liqueur St-James 400ml",
            "prix": 3100
        },
        {
            "produit": "Sac de riz Oncle Sam 50Kg",
            "prix": 18000
        }
        ]
    }
    """

    queryset = models.Client.objects.all()
    serializer_class = ClientSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        client = models.Client.objects.create(client=serializer.data["client"])
        client.save()

        for item in serializer.data["achats"]:
            pd = models.Produit(produit=item.get("produit"), prix=item.get("prix"))
            pd.save()
            client.achats.add(pd.id)
            client.save()

        result = serializers.ClientSerializer(models.Client.objects.all(), many=True)
        return Response(result.data, status=status.HTTP_201_CREATED)
