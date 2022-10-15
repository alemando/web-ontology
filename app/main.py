from rdflib import Graph, BNode

from fastapi import FastAPI
from fastapi import FastAPI, File, HTTPException

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

        classConsult = (
            objectBaseConsult
            % "owl:Class \n FILTER NOT EXISTS {?pizza owl:equivalentClass ?nodo}"
        )
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
        ?pizza %s ?something
        }
        """
        subClassPropertyConsult = predicateBaseConsult % "rdfs:subClassOf"
        equivalentPropertyConsult = predicateBaseConsult % "owl:equivalentClass"
        disjointPropertyConsult = objectBaseConsult % "owl:AllDisjointClasses"
        subPropertyConsult = predicateBaseConsult % "rdfs:subPropertyOf"
        functionalPropertyConsult = predicateBaseConsult % "owl:FunctionalProperty"
        inversePropertyConsult = predicateBaseConsult % "owl:inverseOf"
        transitivePropertyConsult = predicateBaseConsult % "owl:TransitiveProperty"
        asymmetricPropertyConsult = predicateBaseConsult % "owl:AsymmetricProperty"
        symmetricPropertyClassConsult = predicateBaseConsult % "owl:SymmetricProperty"
        irreflexivePropertyConsult = predicateBaseConsult % "owl:IrreflexiveProperty"
        reflexivePropertyConsult = predicateBaseConsult % "owl:ReflexiveProperty"

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
            "DisjointClasses": disjointPropertyConsult,
        }

        for k in metricsAcces:
            metrics[k] += len(list(g.query(metricsAcces[k])))

        return metrics
    except:
        raise HTTPException(status_code=404, detail="Item not found")
