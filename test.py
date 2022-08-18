from rdflib import Graph
import json


g = Graph()
g.parse('ejercicio1.ttl')

a="[\n  {\n    \"@id\": \"http://book.org/books/Hamlet\",\n    \"http://book.org/books/Autor\": [\n      {\n        \"@value\": \"W.Shakespeare\"\n      }\n    ],\n    \"http://book.org/books/Año_Publicacion\": [\n      {\n        \"@type\": \"http://www.w3.org/2001/XMLSchema#gYear\",\n        \"@value\": \"2011\"\n      }\n    ],\n    \"http://book.org/books/Edicion\": [\n      {\n        \"@value\": \"N.D\"\n      }\n    ],\n    \"http://book.org/books/Editorial\": [\n      {\n        \"@value\": \"Simon and Brown\"\n      }\n    ],\n    \"http://book.org/books/ISBN\": [\n      {\n        \"@value\": \"1613820917\"\n      }\n    ],\n    \"http://book.org/books/Idioma\": [\n      {\n        \"@value\": \"Ingles\"\n      }\n    ],\n    \"http://book.org/books/Paginas\": [\n      {\n        \"@value\": 330\n      }\n    ],\n    \"http://book.org/books/Titulo\": [\n      {\n        \"@value\": \"Hamlet\"\n      }\n    ]\n  },\n  {\n    \"@id\": \"http://book.org/books/TheLordOfTheRings\",\n    \"http://book.org/books/Autor\": [\n      {\n        \"@value\": \"J.R.R.Tolkien\"\n      }\n    ],\n    \"http://book.org/books/Año_Publicacion\": [\n      {\n        \"@type\": \"http://www.w3.org/2001/XMLSchema#gYear\",\n        \"@value\": \"2015\"\n      }\n    ],\n    \"http://book.org/books/Edicion\": [\n      {\n        \"@value\": \"Primera\"\n      }\n    ],\n    \"http://book.org/books/Editorial\": [\n      {\n        \"@value\": \"Booket\"\n      }\n    ],\n    \"http://book.org/books/ISBN\": [\n      {\n        \"@value\": \"9789584250681>\"\n      }\n    ],\n    \"http://book.org/books/Idioma\": [\n      {\n        \"@value\": \"Español\"\n      }\n    ],\n    \"http://book.org/books/Paginas\": [\n      {\n        \"@value\": 576\n      }\n    ],\n    \"http://book.org/books/Titulo\": [\n      {\n        \"@value\": \"El Señor de los Anillos\"\n      }\n    ]\n  }\n]"

z = json.load(a)

print(z)