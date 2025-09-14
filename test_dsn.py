#!/usr/bin/env python3
import pyodbc

# Test avec DSN
print("Test de connexion avec DSN...")

# Créer un DSN temporaire
dsn_name = 'TEST_TDB_DSN'

try:
    # Test de connexion avec DSN
    conn_str = f'DSN={dsn_name};UID=Dev_Cube_Web;PWD=G4L|pK$9tbal;'
    conn = pyodbc.connect(conn_str)
    print("✅ Connexion avec DSN réussie !")
    conn.close()
except pyodbc.Error as e:
    print(f"❌ Erreur DSN: {e}")

# Test avec chaîne de connexion complète mais différente
print("\nTest avec format de chaîne différent...")

conn_str = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=172.31.0.5,1433;INSTANCENAME=SAGE_SQL2019;DATABASE=TEST_TDB;UID=Dev_Cube_Web;PWD=G4L|pK$9tbal;TrustServerCertificate=yes;Encrypt=no;'

try:
    conn = pyodbc.connect(conn_str)
    print("✅ Connexion avec INSTANCENAME réussie !")
    
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION")
    version = cursor.fetchone()[0]
    print(f"Version: {version[:50]}...")
    
    conn.close()
except pyodbc.Error as e:
    print(f"❌ Erreur INSTANCENAME: {e}")

# Test avec port dynamique
print("\nTest avec port dynamique...")

try:
    # D'abord, trouver le port de l'instance
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('172.31.0.5', 1433))
    sock.close()
    
    if result == 0:
        print("Port 1433 ouvert")
        # Essayer de se connecter directement au port
        conn_str = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=172.31.0.5,1433;DATABASE=TEST_TDB;UID=Dev_Cube_Web;PWD=G4L|pK$9tbal;TrustServerCertificate=yes;Encrypt=no;'
        conn = pyodbc.connect(conn_str)
        print("✅ Connexion directe au port 1433 réussie !")
        conn.close()
    else:
        print("Port 1433 fermé")
        
except Exception as e:
    print(f"❌ Erreur port: {e}")
