#!/usr/bin/env python3
import pyodbc

# Test avec différents formats de mot de passe
passwords_to_test = [
    'G4L|pK$9tbal',  # Original
    'G4L\\|pK$9tbal',  # Échappement du pipe
    'G4L\\|pK\\$9tbal',  # Échappement du pipe et du dollar
    'G4L\\|pK\\$9tbal',  # Double échappement
    r'G4L|pK$9tbal',  # Raw string
]

server = '172.31.0.5\\SAGE_SQL2019'
database = 'TEST_TDB'
username = 'Dev_Cube_Web'

for i, password in enumerate(passwords_to_test, 1):
    print(f"\n🔍 Test mot de passe {i}: {password}")
    
    conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;Encrypt=no;'
    
    try:
        conn = pyodbc.connect(conn_str)
        print("✅ Connexion réussie !")
        
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        print(f"Version: {version[:50]}...")
        
        conn.close()
        print(f"✅ Mot de passe correct: {password}")
        break
        
    except pyodbc.Error as e:
        print(f"❌ Erreur: {e}")
    except Exception as e:
        print(f"❌ Erreur générale: {e}")

print("\n" + "="*50)
print("Test avec URL encoding...")

# Test avec URL encoding
import urllib.parse
password_encoded = urllib.parse.quote('G4L|pK$9tbal')
print(f"Mot de passe encodé: {password_encoded}")

conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password_encoded};TrustServerCertificate=yes;Encrypt=no;'

try:
    conn = pyodbc.connect(conn_str)
    print("✅ Connexion avec URL encoding réussie !")
    conn.close()
except pyodbc.Error as e:
    print(f"❌ Erreur URL encoding: {e}")
except Exception as e:
    print(f"❌ Erreur générale: {e}")
