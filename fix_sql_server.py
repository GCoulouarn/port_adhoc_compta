#!/usr/bin/env python3
"""
Script pour résoudre le problème de connexion SQL Server avec Django
"""
import pyodbc
import os
import sys

# Ajouter le répertoire du projet au path
sys.path.append('/Users/gillescoulouarn/Dev/port_adhoc_compta')

def test_connection_formats():
    """Test différents formats de connexion"""
    server = '172.31.0.5\\SAGE_SQL2019'
    database = 'TEST_TDB'
    username = 'Dev_Cube_Web'
    password = 'G4L|pK$9tbal'
    
    formats = [
        {
            'name': 'Format 1 - Instance avec backslash',
            'conn_str': f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;Encrypt=no;'
        },
        {
            'name': 'Format 2 - Instance avec double backslash',
            'conn_str': f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER=172.31.0.5\\\\SAGE_SQL2019;DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;Encrypt=no;'
        },
        {
            'name': 'Format 3 - Instance avec virgule',
            'conn_str': f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER=172.31.0.5,1433;INSTANCENAME=SAGE_SQL2019;DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;Encrypt=no;'
        },
        {
            'name': 'Format 4 - Port dynamique',
            'conn_str': f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER=172.31.0.5,1433;DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes;Encrypt=no;'
        }
    ]
    
    working_format = None
    
    for fmt in formats:
        print(f"\n🔍 Test: {fmt['name']}")
        try:
            conn = pyodbc.connect(fmt['conn_str'])
            print("✅ Connexion réussie !")
            
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()[0]
            print(f"Version: {version[:50]}...")
            
            # Test des tables
            cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME LIKE 'T_E_%' ORDER BY TABLE_NAME")
            tables = cursor.fetchall()
            print(f"Tables de comptabilité: {len(tables)}")
            
            conn.close()
            working_format = fmt
            break
            
        except pyodbc.Error as e:
            print(f"❌ Erreur: {e}")
        except Exception as e:
            print(f"❌ Erreur générale: {e}")
    
    return working_format

def create_django_config(working_format):
    """Crée la configuration Django appropriée"""
    if not working_format:
        print("\n❌ Aucun format de connexion ne fonctionne")
        return
    
    print(f"\n✅ Format qui fonctionne: {working_format['name']}")
    print(f"Chaîne de connexion: {working_format['conn_str']}")
    
    # Analyser la chaîne de connexion pour extraire les paramètres
    conn_str = working_format['conn_str']
    
    # Extraire les paramètres
    params = {}
    for part in conn_str.split(';'):
        if '=' in part:
            key, value = part.split('=', 1)
            params[key.strip()] = value.strip()
    
    print(f"\nParamètres extraits:")
    for key, value in params.items():
        print(f"  {key}: {value}")
    
    # Générer la configuration Django
    django_config = """
# Configuration Django pour SQL Server
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'TEST_TDB',
        'USER': 'Dev_Cube_Web',
        'PASSWORD': 'G4L|pK$9tbal',
        'HOST': '172.31.0.5',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'extra_params': 'TrustServerCertificate=yes;Encrypt=no;Trusted_Connection=no;',
            'instance': 'SAGE_SQL2019'
        },
    }
}
"""
    
    print(f"\nConfiguration Django suggérée:")
    print(django_config)

if __name__ == "__main__":
    print("🔧 Résolution du problème de connexion SQL Server")
    print("=" * 50)
    
    working_format = test_connection_formats()
    create_django_config(working_format)
