import sqlite3

# Se connecter à la base
conn = sqlite3.connect("parking.db")
cursor = conn.cursor()

# Vérifier les tables existantes
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables existantes :", tables)

# Vérifier le contenu de la table cars
cursor.execute("SELECT * FROM cars")
cars = cursor.fetchall()
print("Contenu de la table cars :", cars)

conn.close()