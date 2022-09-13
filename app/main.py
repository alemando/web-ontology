from rdflib import Graph

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
