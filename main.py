from dataclasses import Field
import tempfile
import shutil
from rdflib import Graph

from pydantic import BaseModel
from fastapi import FastAPI, Body

app = FastAPI()

##Models 

# class Ontology(BaseModel):
#     direction: str = Field(...,
#                            example= 'archivo.ttl')

g=Graph()

@app.post("/post")

def postOntology(
    onto = Body(...)
):
    g.parse(onto)
    tempdir = tempfile.mkdtemp(prefix="myapplication-")
    return g.serialize(format='json-ld')
    
@app.get("/read", status_code=201)

def readOntology():
    return g





