#!/usr/bin/env python3
"""
Script de test de connexion à SQL Server
"""
import pyodbc
import sys

def test_connection():
    """Teste la connexion à SQL Server"""
    try:
        # Chaîne de connexion avec différentes options
        connection_strings = [
            # Option 1: Driver 18 avec TrustServerCertificate
            "DRIVER={ODBC Driver 18 for SQL Server};SERVER=192.168.152.26,1433;DATABASE=PAD_TDB;UID=gcoulouarn;PWD=raw3te7@ga1#No5;TrustServerCertificate=yes;Encrypt=no;",
            
            # Option 2: Driver 17 avec TrustServerCertificate
            "DRIVER={ODBC Driver 17 for SQL Server};SERVER=192.168.152.26,1433;DATABASE=PAD_TDB;UID=gcoulouarn;PWD=raw3te7@ga1#No5;TrustServerCertificate=yes;Encrypt=no;",
            
            # Option 3: Driver 18 avec Encrypt=optional
            "DRIVER={ODBC Driver 18 for SQL Server};SERVER=192.168.152.26,1433;DATABASE=PAD_TDB;UID=gcoulouarn;PWD=raw3te7@ga1#No5;Encrypt=optional;TrustServerCertificate=yes;",
        ]
        
        for i, conn_str in enumerate(connection_strings, 1):
            print(f"\n=== Test de connexion {i} ===")
            print(f"Chaîne: {conn_str[:50]}...")
            
            try:
                conn = pyodbc.connect(conn_str)
                cursor = conn.cursor()
                cursor.execute("SELECT @@VERSION")
                version = cursor.fetchone()[0]
                print(f"✅ Connexion réussie!")
                print(f"Version SQL Server: {version[:50]}...")
                conn.close()
                return conn_str
            except Exception as e:
                print(f"❌ Échec: {e}")
        
        print("\n❌ Aucune connexion n'a fonctionné")
        return None
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        return None

if __name__ == "__main__":
    print("Test de connexion à SQL Server...")
    print("Serveur: 192.168.152.26:1433")
    print("Base: PAD_TDB")
    print("Utilisateur: gcoulouarn")
    
    working_connection = test_connection()
    
    if working_connection:
        print(f"\n✅ Chaîne de connexion qui fonctionne:")
        print(working_connection)
    else:
        print("\n❌ Aucune connexion n'a fonctionné. Vérifiez:")
        print("1. Que le serveur SQL Server est accessible")
        print("2. Que les identifiants sont corrects")
        print("3. Que les drivers ODBC sont installés")
        print("4. Que le port 1433 est ouvert")
