# SUPER PRIX API

## Recuperation

`git clone https://github.com/elysee-01/superprix.git`

## Excecution

`cd superprix/`

`python3 -m pip install requirements.txt`

`python3 manage.py runserver`

## Endpoints

1. Montant le plus eleve

> GET: /montant_plus_eleve/

2. Prix de vente

> GET: /prix_vente/<client_ID>/

3. Ajout de nouveau client

> POST: /add-client/


:: Exemple

POST:
```JSON

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

```