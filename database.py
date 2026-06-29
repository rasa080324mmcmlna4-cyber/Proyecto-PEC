from pymongo import MongoClient

cliente = MongoClient("mongodb://localhost:27017/")

db = cliente["ecoruta"]

usuarios = db["usuarios"]
residuos = db["residuos"]
puntos = db["puntos_recoleccion"]
campanas = db["campanas"]
reportes = db["reportes"]