
import os
import sqlite3


class DB_Management:
    # Constructeur
    def __init__(self, path):
        try:
            self.conn = sqlite3.connect(path)
        except Exception:
            print('Error detected, impossible to connect to the database sorry')
            self.echec=1
        else:
            self.cursor = self.conn.cursor()
            self.echec=0
    
    def createTables(self, dicTables):
        # On va parcourir les tables du dictable
        for table in dicTables:
            req = "CREATE TABLE IF NOT EXISTS %s (" % table
            pk =''
            for descr in dicTables[table]:
                nomChamp = descr[0]     # libellé du champ à créer
                tch = descr[1]          # type de champ à créer
                if tch =='f':           # champ FLOAT
                    typeChamp = 'FLOAT'
                elif tch =='k':         # champ primary key              
                    typeChamp = 'INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE'
                    pk = nomChamp
                else:                   # champ TEXT
                    typeChamp = 'TEXT'
                req = req + nomChamp + ' ' + typeChamp +','
            req = req[:-1] + ')'
            # la requete devrait être ok
            print(req)
            self.cursor.execute(req)
        
    def get_table_list(self):
        _SQL = """SELECT name FROM sqlite_master
        WHERE type='table'
        ORDER BY name"""
        self.cursor.execute(_SQL)
        results = self.cursor.fetchall()
        table_list = [
            v[0] for v in results
            if v[0] != "sqlite_sequence"
        ]
        print("voici toutes les tables:", table_list)
        return table_list
    
    def clean_table(self, table):
        self.cursor.execute("DELETE FROM " +table+"")
        print ("table ", table, "vidée")
    
    def clean_all_tables(self):
        table_list = self.get_table_list()
        for table in table_list:
            self.clean_table(table)

    def show_table(self, table):
        self.cursor.execute("SELECT * from "+table+"")
        for line in self.cursor.fetchall():
            print(line)

    def delete_table(self, table):
        # suppression de la table
        self.cursor.execute("DROP TABLE " +table+"")
        print ("table ", table, "supprimée")
#        self.commit()

    def delete_all_tables(self):
        table_list = self.get_table_list()
        for table in table_list:
            self.delete_table(table)
        print('Tables supprimées')

    # This function has not been tested. It is not used yet
    def select_table(self, table):
        req = "SELECT * from %s" % table
        self.cursor.execute(req)




    
        
