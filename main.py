import requests
import json

# A r B -> je cherche un C tq A r_isa C et C r B.
# Il faut préciser le schéma d'inférence. A r C et C r B peut être suffisant.

relations = {
    "r_isa" : "6",
    "r_agent-1": "24"
}

def testRel(node1, node2, rel):
    urlR = "https://jdm-api.demo.lirmm.fr/v0/relations/from/" + node1 + "/to/" + node2 + "?types_ids=" + rel

    r = requests.get(urlR)
    return r.json()

def getIsas(node):
    res = requests.get("https://jdm-api.demo.lirmm.fr/v0/relations/from/"+node+"?types_ids=6").json()
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

    nodes,rels = getIsas(node1)

    rels.sort(key=lambda x: x['w'], reverse=True)

    test=0
    for e in rels:
        node2Rel = getNode2(e['node2'], nodes)
        local = testRel(node2Rel['name'], node2, "24")
        if local.get('nodes'):
            finalC = node2Rel['name']
            test = 1
            break
        else:
            print("NO")

    if test:
        print(node1 + " " + rel + " " + node2 + " => Oui | "+node1+" r_isa "+finalC+" & "+finalC+" r_agent-1 "+node2)
        return 1

    return 0

# https://jdm-api.demo.lirmm.fr/v0/node_by_name/{node1_name}
# https://jdm-api.demo.lirmm.fr/v0/relations/from/{node1_name}/to/{node2_name}
main()
