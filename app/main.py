from rdflib import Graph, BNode
import rdflib
from fastapi import FastAPI
from fastapi import FastAPI, File, HTTPException


###########################
# General hierarchy function
###############################


def getHierarchy(parents: list, childs: list, absoluteParent: str, relation):

    """
    Parents are the superclasses and childs their subclasses;
        for example parents is a list of Classes and childs are the list of subclasses of a graph
    absoluteParent is the parent of everything that has not an explicit parent class
        for example: http://www.w3.org/2002/07/owl#/Thing
    relation is a variable that specifies the rdflib propertie that will define the tree hierarchy
        for example: rdflib.RDFS.subClassOf
    """

    absoluteParentChilds = []
    exclusiveParents = [
        element
        for element in parents + childs
        if element in parents and element not in childs
    ]
    print(exclusiveParents)
    for i in exclusiveParents:
        tree = rdflib.util.get_tree(
            g,
            rdflib.URIRef(i),
            relation,
            mapper=lambda x: (x),
        )
        absoluteParentChilds.append(tree)

    generalTree = {absoluteParent: absoluteParentChilds}

    return generalTree


##############################
# Define metrics and querys structures
#####################################
metrics = {
    "Class": 0,
    "ObjectProperty": 0,
    "DataProperty": 0,
    "Individual": 0,
    "Subclass": 0,
    "DisjointClasses": 0,
    "EquivalentClass": 0,
    "SubObjectProperty": 0,
    "Inverse": 0,
    "FunctionalProperty": 0,
    "TransitiveProperty": 0,
    "AsymmetricProperty": 0,
    "SymmetricProperty": 0,
    "IrreflexiveProperty": 0,
    "ReflexiveProperty": 0,
}

## object querys
objectBaseConsult = """
PREFIX : <http://www.pizzaowl.org#>
PREFIX owl: <http://www.w3.org/2002/07/owl#> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
SELECT DISTINCT ?pizza WHERE { 
?pizza rdf:type %s
}
"""

classConsult = objectBaseConsult % "owl:Class \n FILTER isURI(?pizza)."
objectPropertyConsult = objectBaseConsult % "owl:ObjectProperty"
individualConsult = objectBaseConsult % "owl:NamedIndividual"
dataPropertyConsult = objectBaseConsult % "owl:DatatypeProperty"
# disjointClassConsult = objectBaseConsult % "owl:AllDisjointClasses"

## predicate querys
predicateBaseConsult = """
PREFIX : <http://www.pizzaowl.org#>
PREFIX owl: <http://www.w3.org/2002/07/owl#> 
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
SELECT ?pizza WHERE { 
?pizza %s
}
"""
subClassPropertyConsult = (
    predicateBaseConsult % "rdfs:subClassOf  ?something \n FILTER isURI(?something)."
)
equivalentPropertyConsult = predicateBaseConsult % "owl:equivalentClass ?something."
disjointPropertyConsult = objectBaseConsult % "owl:AllDisjointClasses ?something."
subPropertyConsult = predicateBaseConsult % "rdfs:subPropertyOf ?something."
functionalPropertyConsult = predicateBaseConsult % "owl:FunctionalProperty ?something."
inversePropertyConsult = predicateBaseConsult % "owl:inverseOf ?something."
transitivePropertyConsult = predicateBaseConsult % "owl:TransitiveProperty ?something."
asymmetricPropertyConsult = predicateBaseConsult % "owl:AsymmetricProperty ?something."
symmetricPropertyClassConsult = (
    predicateBaseConsult % "owl:SymmetricProperty ?something."
)
irreflexivePropertyConsult = (
    predicateBaseConsult % "owl:IrreflexiveProperty ?something."
)
reflexivePropertyConsult = predicateBaseConsult % "owl:ReflexiveProperty ?something."

metricsAcces = {
    "Class": classConsult,
    "Individual": individualConsult,
    "DataProperty": dataPropertyConsult,
    "ObjectProperty": objectPropertyConsult,
    "Subclass": subClassPropertyConsult,
    "EquivalentClass": equivalentPropertyConsult,
    "SubObjectProperty": subPropertyConsult,
    "FunctionalProperty": functionalPropertyConsult,
    "Inverse": inversePropertyConsult,
    "TransitiveProperty": transitivePropertyConsult,
    "AsymmetricProperty": asymmetricPropertyConsult,
    "SymmetricProperty": symmetricPropertyClassConsult,
    "ReflexiveProperty": reflexivePropertyConsult,
    "IrreflexiveProperty": irreflexivePropertyConsult,
    # "DisjointClasses": disjointPropertyConsult,
}


thing = "https://www.w3.org/2002/07/owl#/Thing"
topObjectProperty = "https://www.w3.org/2002/07/owl#/topObjectProperty"
topDataProperty = "https://www.w3.org/2002/07/owl#/topDataProperty"

###################################
# App structure
#########################################

app = FastAPI()
g = Graph()


@app.post("/files/")
async def create_file(file: bytes = File()):
    try:
        g.parse(file)
    except:
        raise HTTPException(status_code=400, detail="Invalid file")
    return "ok"


@app.get(
    "/",
    responses={
        404: {"description": "Item not found"},
    },
)
async def root():
    some = True
    if some:
        return {"msg": "Hello World"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get(
    "/metrics/",
    responses={
        404: {"description": "Item not found"},
    },
)
async def root():
    try:
        for k in metricsAcces:
            metrics[k] += len(list(g.query(metricsAcces[k])))
            print(k)
        return metrics
    except:
        raise HTTPException(status_code=404, detail="Item not found")


##############
# Classes and subclasess hierarchy
##############


@app.get(
    "/classesHierarchy/",
    responses={
        404: {"description": "Item not found"},
    },
)
async def root():
    try:

        Clases = [x[0] for x in list(g.query(metricsAcces["Class"]))]
        Subclases = [x[0] for x in list(g.query(metricsAcces["Subclass"]))]

        return getHierarchy(Clases, Subclases, thing, rdflib.RDFS.subClassOf)

    except:
        raise HTTPException(status_code=404, detail="Item not found")


# ##############
# # Object Properties
# ##############


@app.get(
    "/objectPropertiesHierarchy/",
    responses={
        404: {"description": "Item not found"},
    },
)
async def root():
    try:

        Property = [x[0] for x in list(g.query(metricsAcces["ObjectProperty"]))]
        SubProperty = [x[0] for x in list(g.query(metricsAcces["SubObjectProperty"]))]

        return getHierarchy(
            Property, SubProperty, topObjectProperty, rdflib.RDFS.subPropertyOf
        )

    except:
        raise HTTPException(status_code=404, detail="Item not found")


# #############
# # Data Properties
# ##############


@app.get(
    "/dataPropertiesHierarchy/",
    responses={
        404: {"description": "Item not found"},
    },
)
async def root():
    try:

        Property = [x[0] for x in list(g.query(metricsAcces["DataProperty"]))]
        SubProperty = [x[0] for x in list(g.query(metricsAcces["SubObjectProperty"]))]

        return getHierarchy(
            Property, SubProperty, topDataProperty, rdflib.RDFS.subPropertyOf
        )

    except:
        raise HTTPException(status_code=404, detail="Item not found")
