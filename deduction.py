import requests
import json

# A R B
# A r1 C, C r2 B
# l'un des deux r est r_isa

def getIsas(node : str) -> None:
    """donne la liste des node isa X, relations en poids décroissant"""
    res = requests.get("https://jdm-api.demo.lirmm.fr/v0/relations/from/"+node+"?types_ids=6").json()
    res['relations'].sort(key=lambda x: x['w'], reverse=True)
    with open("r_isas/"+ node +".json", "w", encoding="utf-8") as f:
            json.dump(res, f, indent=4, ensure_ascii=False)

def deduction() -> int:
    print("Bonjour, entrez votre requête :")
    requete = input(str())
    array = requete.split()
    # TODO : changer le split " " en split "r_"
    
    # TODO
    node1 = array[0]
    node2 = array[2]
    rel = array[1]

    if len(array) != 3:
        print("PAS FAIT")
        return -1

    # Etape 1 : A r_isa C, C rel B
    getIsas(node1)

    # Etape 2 : A rel C, C isa B
    


getIsas("pigeon")