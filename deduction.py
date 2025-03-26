import requests
import json
import os
import time
from math import sqrt
from main import getNode2, testRelation, getRelId

# A R B
# A r1 C, C r2 B
# l'un des deux r est r_isa

def getIsas(node : str) -> int:
    """donne la liste des node isa X, relations en poids décroissant"""

    filename = "r_isas/"+ node +".json"
    if os.path.exists(filename):
        file_age = time.time() - os.path.getmtime(filename)
        if file_age < 86400:
            # Fichier moins de 24h
            return 0
        else:
            # MaJ fichier
            res = requests.get("https://jdm-api.demo.lirmm.fr/v0/relations/from/"+node+"?types_ids=6").json()
            res['relations'].sort(key=lambda x: x['w'], reverse=True)
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(res, f, indent=4, ensure_ascii=False)
            return 2
    else:
        # Creation fichier
        res = requests.get("https://jdm-api.demo.lirmm.fr/v0/relations/from/"+node+"?types_ids=6").json()
        res['relations'].sort(key=lambda x: x['w'], reverse=True)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(res, f, indent=4, ensure_ascii=False)
        return 1


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
    print(getIsas(node1))

    with open("r_isas/"+node1+".json", "r", encoding="utf-8") as f:
        data = json.load(f)

    test = 0
    maxW = 0
    for relation in data['relations']:
        w1 = relation['w']
        if w1 < 0:
            pass
        node2relation = getNode2(relation['node2'],data['nodes'])
        local = testRelation(node2relation['name'], node2, getRelId(rel))
        if local.get('nodes'):
            w2 = local['relations'][0]['id']
            if (w1 * w2) > 0:
                if sqrt(w1*w2) > maxW:
                    finalC = node2relation['name']
                    maxW = sqrt(w1*w2)
                    print("new max = "+str(maxW))
                    test = 1
            else:
                pass
    
    if test:
        print(node1 + " " + rel + " " + node2 + " => Oui | "+node1+" r_isa "+finalC+" & "+finalC+" r_agent-1 "+node2 + " | score")
        return 1
    else:
        print("No result")


    # Etape 2 : A rel C, C isa B
    return 0

deduction()