from pymongo import MongoClient

cliente = MongoClient("mongodb+srv://rasa080324mmcmlna4_db_user:<db_password>@cluster0.vefrpla.mongodb.net/?appName=Cluster0")

db = cliente["ecoruta"]

usuarios = db["usuarios"]
residuos = db["residuos"]
puntos = db["puntos_recoleccion"]
campanas = db["campanas"]
reportes = db["reportes"]