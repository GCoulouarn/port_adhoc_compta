#!/usr/bin/env python3
import pyodbc

# Paramètres de connexion
server = '172.31.0.5\\SAGE_SQL2019'
database = 'TEST_TDB'
username = 'Dev_Cube_Web'
password = 'G4L|pK$9tbal'

# Chaîne de connexion
connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;Encrypt=no;'

print("Test de connexion directe avec pyodbc...")
print(f"Server: {server}")
print(f"Database: {database}")
print(f"Username: {username}")

try:
    # Tentative de connexion
    conn = pyodbc.connect(connection_string)
    print("✅ Connexion réussie !")
    
    # Test d'une requête simple
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION")
    version = cursor.fetchone()[0]
    print(f"Version SQL Server: {version[:100]}...")
    
    # Test des tables
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' ORDER BY TABLE_NAME")
    tables = cursor.fetchall()
    print(f"\n📊 Tables trouvées ({len(tables)}):")
    for table in tables[:10]:
        print(f"  - {table[0]}")
    
    conn.close()
    print("\n✅ Test de connexion terminé avec succès !")
    
except pyodbc.Error as e:
    print(f"❌ Erreur pyodbc: {e}")
except Exception as e:
    print(f"❌ Erreur générale: {e}")
