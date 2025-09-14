#!/usr/bin/env python3
import pyodbc

# Test avec différents formats de chaîne de connexion
configs = [
    {
        'name': 'Format 1 - Échappement simple',
        'conn_str': 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=172.31.0.5\\SAGE_SQL2019;DATABASE=TEST_TDB;UID=Dev_Cube_Web;PWD=G4L|pK$9tbal;TrustServerCertificate=yes;Encrypt=no;'
    },
    {
        'name': 'Format 2 - Échappement double',
        'conn_str': 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=172.31.0.5\\\\SAGE_SQL2019;DATABASE=TEST_TDB;UID=Dev_Cube_Web;PWD=G4L|pK$9tbal;TrustServerCertificate=yes;Encrypt=no;'
    },
    {
        'name': 'Format 3 - Sans échappement',
        'conn_str': 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=172.31.0.5/SAGE_SQL2019;DATABASE=TEST_TDB;UID=Dev_Cube_Web;PWD=G4L|pK$9tbal;TrustServerCertificate=yes;Encrypt=no;'
    },
    {
        'name': 'Format 4 - Avec port explicite',
        'conn_str': 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=172.31.0.5,1433;INSTANCENAME=SAGE_SQL2019;DATABASE=TEST_TDB;UID=Dev_Cube_Web;PWD=G4L|pK$9tbal;TrustServerCertificate=yes;Encrypt=no;'
    }
]

for config in configs:
    print(f"\n🔍 Test: {config['name']}")
    print(f"Chaîne: {config['conn_str'][:80]}...")
    
    try:
        conn = pyodbc.connect(config['conn_str'])
        print("✅ Connexion réussie !")
        
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        print(f"Version: {version[:50]}...")
        
        conn.close()
        break  # Arrêter au premier succès
        
    except pyodbc.Error as e:
        print(f"❌ Erreur: {e}")
    except Exception as e:
        print(f"❌ Erreur générale: {e}")

print("\n" + "="*50)
print("Test de connexion avec différents utilisateurs...")

# Test avec d'autres utilisateurs possibles
users_to_test = [
    'Dev_Cube_Web',
    'dev_cube_web', 
    'Dev_Cube_Web@172.31.0.5',
    'Dev_Cube_Web@172.31.0.5\\SAGE_SQL2019'
]

for user in users_to_test:
    print(f"\n🔍 Test utilisateur: {user}")
    conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER=172.31.0.5\\SAGE_SQL2019;DATABASE=TEST_TDB;UID={user};PWD=G4L|pK$9tbal;TrustServerCertificate=yes;Encrypt=no;'
    
    try:
        conn = pyodbc.connect(conn_str)
        print("✅ Connexion réussie !")
        conn.close()
        break
    except pyodbc.Error as e:
        print(f"❌ Erreur: {e}")
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
