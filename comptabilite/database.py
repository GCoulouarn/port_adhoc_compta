"""
Configuration de base de données personnalisée pour Django mssql
"""
import pyodbc
from django.db.backends.base.base import BaseDatabaseWrapper
from django.db.backends.base.operations import BaseDatabaseOperations
from django.db.backends.base.client import BaseDatabaseClient
from django.db.backends.base.creation import BaseDatabaseCreation
from django.db.backends.base.introspection import BaseDatabaseIntrospection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.backends.mssql.base import DatabaseWrapper as MSSQLDatabaseWrapper
from django.db.backends.mssql.operations import DatabaseOperations
from django.db.backends.mssql.client import DatabaseClient
from django.db.backends.mssql.creation import DatabaseCreation
from django.db.backends.mssql.introspection import DatabaseIntrospection
from django.db.backends.mssql.schema import DatabaseSchemaEditor


class CustomMSSQLDatabaseWrapper(MSSQLDatabaseWrapper):
    """
    Wrapper personnalisé pour MSSQL avec gestion de l'instance
    """
    
    def get_connection_params(self):
        """Override pour gérer l'instance SQL Server"""
        settings_dict = self.settings_dict
        options = settings_dict.get('OPTIONS', {})
        
        # Construction de la chaîne de connexion personnalisée
        conn_params = {
            'driver': options.get('driver', 'ODBC Driver 18 for SQL Server'),
            'server': settings_dict['HOST'],
            'database': settings_dict['NAME'],
            'uid': settings_dict['USER'],
            'pwd': settings_dict['PASSWORD'],
            'trusted_connection': 'no',
            'encrypt': 'no',
            'trustservercertificate': 'yes',
        }
        
        # Ajouter l'instance si spécifiée
        if 'instance' in options:
            conn_params['server'] = f"{settings_dict['HOST']}\\{options['instance']}"
        
        return conn_params
    
    def create_cursor(self, name=None):
        """Override pour utiliser notre chaîne de connexion personnalisée"""
        if self.connection is None:
            self.connection = self.get_new_connection(self.get_connection_params())
        return self.connection.cursor()
    
    def get_new_connection(self, conn_params):
        """Créer une nouvelle connexion avec pyodbc"""
        # Construction de la chaîne de connexion
        conn_str_parts = []
        for key, value in conn_params.items():
            if key == 'driver':
                conn_str_parts.append(f"DRIVER={{{value}}}")
            elif key == 'server':
                conn_str_parts.append(f"SERVER={value}")
            elif key == 'database':
                conn_str_parts.append(f"DATABASE={value}")
            elif key == 'uid':
                conn_str_parts.append(f"UID={value}")
            elif key == 'pwd':
                conn_str_parts.append(f"PWD={value}")
            elif key == 'trusted_connection':
                conn_str_parts.append(f"Trusted_Connection={value}")
            elif key == 'encrypt':
                conn_str_parts.append(f"Encrypt={value}")
            elif key == 'trustservercertificate':
                conn_str_parts.append(f"TrustServerCertificate={value}")
        
        conn_str = ';'.join(conn_str_parts)
        
        # Connexion avec pyodbc
        return pyodbc.connect(conn_str)
