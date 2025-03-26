import requests
import json

# A r B -> je cherche un C tq A r_isa C et C r B.
# Il faut préciser le schéma d'inférence. A r C et C r B peut être suffisant.

# socring, sqrt(score a * score b)

# mettre en cache dans un json les résultats de requetes



relations = {
    "r_isa" : "6",
    "r_agent-1": "24"
}

def testRel(node1, node2, rel):
    urlR = "https://jdm-api.demo.lirmm.fr/v0/relations/from/" + node1 + "/to/" + node2 + "?types_ids=" + rel

    r = requests.get(urlR)
    return r.json()

# modifier pour toutes les relations !
def getIsas(node):
    rel = "6"
    #trouve les r_isa
    res = requests.get("https://jdm-api.demo.lirmm.fr/v0/relations/from/"+node+"?types_ids="+rel).json()
    nodes = res['nodes']
    rels = res['relations']
    return nodes,rels

def getName(node, nodes):
    for elem in nodes:
        if e['id'] == node:
            return e['name']

def getNode2(id, nodes):
    for elem in nodes:
        if elem['id'] == id:
            return elem
    return 0

def main():
    init()
    print("Bonjour, entrez votre requête :")
    requete = input(str())
    array = requete.split()
    # TODO : changer le split " " en split "r_"
    
    # TODO
    node1 = array[0]
    node2 = array[2]
    rel = relations[array[1]]

    if len(array) != 3:
        print("PAS FAIT")
        return -1

    # déduction
    nodes,rels = getIsas(node1)
    # rels = listes des node1 r_isa X
    # Je dois faire avec autre chose que les isas ? enorme ?

    rels.sort(key=lambda x: x['w'], reverse=True)
    # vérif si négatif?

    test=0
    for e in rels:
        if e['w'] < 100:
            pass
        else:
            node2Rel = getNode2(e['node2'], nodes)
            local = testRel(node2Rel['name'], node2, rel)
            if local.get('nodes'):
                finalC = node2Rel['name']
                test = 1
                break
            else:
                pass

    if test:
        print(node1 + " " + rel + " " + node2 + " => Oui | "+node1+" r_isa "+finalC+" & "+finalC+" r_agent-1 "+node2 + " | score")
        return 1
    else:
        print("No result")

    return 0



def init():
    res = requests.get("https://jdm-api.demo.lirmm.fr/v0/relations_types").json()
    with open("relations.json", "w", encoding="utf-8") as f:
            json.dump(res, f, indent=4, ensure_ascii=False)
            

def getRelId(rel):
    with open("relations.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    name_to_id = {item["name"]: item["id"] for item in data}

    return str(name_to_id.get(rel))

# récup toutes les relations, pour vérifier plus tard ?
def getRelsOfNode(node):
    with open("relations.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    name_to_id = {item["name"]: item["id"] for item in data}

    for i in name_to_id:
        res = requests.get("https://jdm-api.demo.lirmm.fr/v0/relations/from/"+node+"?types_ids="+rel).json()
        nodes = res['nodes']
        rels = res['relations']
    
    return nodes,rels

    

"""
res = requests.get("https://jdm-api.demo.lirmm.fr/v0/relations/from/pigeon").json()
with open("pigeon.json", "w", encoding="utf-8") as f:
    json.dump(res, f, indent=4, ensure_ascii=False)
"""
# https://jdm-api.demo.lirmm.fr/v0/node_by_name/{node1_name}
# https://jdm-api.demo.lirmm.fr/v0/relations/from/{node1_name}/to/{node2_name}
main()
