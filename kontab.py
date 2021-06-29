# coding: utf-8
import os
import sqlite3
import csv
import argparse

# local modules
from config import Glob
from model.model import Category, Operation

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
        results = cursor.fetchall()
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
        for line in cursor.fetchall():
            print(line)

    def delete_table(self, table):
        # suppression de la table
        self.cursor.execute("DROP TABLE " +table+"")
        print ("table ", table, "supprimée")

    def delete_all_tables(self):
        table_list = self.get_table_list()
        for table in table_list:
            self.delete_table(table)
        print('Tables supprimées')


# if os.path.isfile(Glob.DB_PATH):
#    print("c'est un fichier")
#else:
#    print("la db n'existe pas, créez un fichier kontab.db")

#conn = sqlite3.connect(Glob.DB_PATH)
db = DB_Management(Glob.DB_PATH)
conn = db.conn
cursor = db.cursor

def init_db():
    #cursor = conn.cursor()
    #cursor = curs
    db.delete_all_tables()
    db.createTables(Glob.dicoT)

    conn.commit()
    db.get_table_list()
    print('Tables crées')

def remplir_donnees_test():
    #Insertion des catégories
    cursor.execute("""
    INSERT into categories (nom, categ_parent) VALUES(?,?)
    """, ("loyer", "habitation"))

    cursor.execute("""
    INSERT into categories(nom, categ_parent) VALUES(?,?)
    """, ("edf", "habitation"))

    conn.commit()
    print('Table categorie initialisée')

    #Insertion de données dans compte
    cursor.execute("""
    INSERT INTO comptes (date_operation, date_valeur, libelle, montant_credit, montant_debit) VALUES(?, ?, ?, ?, ?)
    """, ("03/04/2020", "03/02/2020", "FACTURE EDF", "95", "0"))
    
    cursor.execute("""
    INSERT INTO comptes (date_operation, date_valeur, libelle, montant_credit, montant_debit) VALUES(?, ?, ?, ?, ?)
    """, ("23/03/2020", "23/03/2020", "TELEPHONE", "19", "0"))

    conn.commit()
    print("Table compte initialisée")

    #Insertion de de données dans cerveau
    cursor.execute("""
    INSERT INTO cerveau (libelle, categorie) VALUES(?, ?)
    """, ("FACTURE EDF", "edf"))
    
    cursor.execute("""
    INSERT INTO cerveau (libelle, categorie) VALUES(?, ?)
    """, ("ECH PRET 0909312735306", "loyer"))

    cursor.execute("""
    INSERT INTO cerveau (libelle, categorie) VALUES(?, ?)
    """, ("LAURENCE F. VINCENNES", "coiffeur"))

    db.get_table_list()
    conn.commit()
    print("Table cerveau initialisée")

def vider_tables():
    db.clean_all_tables()
    conn.commit()
    print('Tables vidées')
    
def charger_comptes(fichier):
    # liste_lignes[]
    file = open(fichier, 'r')
    reader = csv.DictReader(file, delimiter=";")
    for row in reader:
        #print(row)
        print(row['Date operation'])
        print(row['Date valeur'])
        print(row['Libelle'])
        print(row['Debit'])
        print(row['Credit'])
        # liste_lignes.append({})

        # On essaie de mettre ça en base
        cursor.execute("""
        INSERT INTO comptes (date_operation, date_valeur, libelle, montant_credit, montant_debit) VALUES(?, ?, ?, ?, ?)
        """, (row['Date operation'], row['Date valeur'], row['Libelle'], row['Debit'], row['Credit']))

    print('on va afficher a nouveau la db')
    conn.commit()
    db.show_table('comptes')

def charger_categories(fichier):
    file = open(fichier,'r')
    reader = csv.DictReader(file, delimiter=";")
    for row in reader:
        cursor.execute("""
        INSERT INTO categories (nom, categ_parent) VALUES(?, ?)
        """, (row['categorie'], row['categorie_parent'])
        )
    print('on va afficher a nouveau les categories')
    conn.commit()
    #liste_categories()
    db.show_table('categories')

def charger_cerveau(fichier):
    #cursor = conn.cursor()
    # liste_lignes[]
    file = open(fichier, 'r')
    reader = csv.DictReader(file, delimiter=";")
    for row in reader:
        # On essaie de mettre ça en base
        
        cursor.execute("""
        INSERT INTO cerveau (libelle, categorie) VALUES(?, ?)
        """, (row['Libelle'], row['Categorie'])
        )
    print('on va afficher a nouveau le cerveau')
    conn.commit()
    db.show_table('cerveau')

def sauvegarder_categories(fichier):
    # file = open('kontabapp/bckp_categories.csv', 'w')
    file = open(fichier, 'w')
    f_csv = csv.writer(file, delimiter=";")
    #f_csv.writerow(en_tetes)
    f_csv.writerow( ('Id','Catégorie','Catégorie parent'))
    
    #cursor = conn.cursor()
    cursor.execute("""
    SELECT * from categories
    """)
    for categ in cursor.fetchall():
        f_csv.writerow(categ)

def sauvegarder_cerveau(fichier):
    # file = open('kontabapp/bckp_cerveau.csv', 'w')
    file = open(fichier, 'w')
    f_csv = csv.writer(file, delimiter=";")
    #f_csv.writerow(en_tetes)
    f_csv.writerow( ('Id','Libéllés','Catégorie'))
    
    #cursor = conn.cursor()
    cursor.execute("""
    SELECT * from cerveau
    """)
    for souvenir in cursor.fetchall():
        f_csv.writerow(souvenir)

def sauvegarder_comptes(fichier):
    # file = open('kontabapp/comptestecr.csv', 'w')
    file = open(fichier, 'w')

    # with open('stocks.csv','w') as f:
    f_csv = csv.writer(file, delimiter=";")
    #f_csv.writerow(en_tetes)
    f_csv.writerow( ('Id','Date operation','Date valeur','Libelle','Debit','Credit','Categorie'))
    
    #cursor = conn.cursor()
    cursor.execute("""
    SELECT * from comptes
    """)
    for ecriture in cursor.fetchall():
        #print(ecriture)
        f_csv.writerow (ecriture)

def rechercher_cerveau(libelle):
    # On va parcourir toute la table cerveau 
    #cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM cerveau
    """
    )
    for souvenir in cursor.fetchall():
        #souvenir : une ligne de la table cerveau
        # Pour chaque ligne on va voir si cerveau.libeelle est existe dans libelle (passé en param)
        result = None
        if souvenir[1] in libelle:
            print(libelle)
            print(souvenir[1])
            print(souvenir[2])
            result = souvenir[2]
            break
    # si on a rien trouver on renvoie result
    return result

def rechercher_categorie(categ):    
    cursor.execute("""
    SELECT * FROM categories where nom=?
    """, (categ,)
    )
    result = cursor.fetchone() 
    if result:
        print('la categorie existe')
        return True
    else:
        print('la categorie existe PAAAS')
        return False

def verifier_categories_cerveau():
    # On va parcourir toute la table cerveau 
    #cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM cerveau
    """
    )
    for souvenir in cursor.fetchall():
        #souvenir : une ligne de la table cerveau
        # Pour chaque ligne on va chercher si la categorie existe bien
        # result = None
        print(souvenir[2])
        rechercher_categorie(souvenir[2])
    
def is_a_category(categ):
    # returns true if categ is present in CATEGORIES table
    #cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM categories where nom=?
    """, (categ,)
    )
    result = cursor.fetchone() 
    if result:
        return True
    else:
        return False

def assigner_categorie(id, categorie):
    #cursor = conn.cursor()
    cursor.execute("""
    UPDATE comptes SET categorie = ? WHERE id_compt = ?
    """, (categorie, id)
    )
    conn.commit()

def assigner_souvenir(libelle, categorie):
    #cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO cerveau (libelle, categorie) VALUES(?, ?)
    """, (libelle, categorie)
    )
    conn.commit()

def parser_comptes():
    print('On va parcourir compte et checker si ya des choses dans cerveau:')
    #cursor = conn.cursor()
    cursor.execute("""
    SELECT * from comptes
    """)
    for ecriture in cursor.fetchall():
        #print(ecriture[3])
        libelle = ecriture[3]
        id = ecriture[0]
        print(id)
        #print(libelle)
        #libe = 'ELECTRIITE'
        #if libelle != None:
        if ecriture[6] == None:
            categ = rechercher_cerveau(libelle)
            if categ != None:
                print("on a trouvé une catégorie dans cerveau")
                assigner_categorie(id, categ)
        #if connu != None:
        #    print('retrouvé')

def parser_compte_manuel():
    #cursor = conn.cursor()
    cursor.execute("""
    SELECT * from comptes
    """)
    for ecriture in cursor.fetchall():
        date_operation = ecriture[1]
        libelle = ecriture[3]
        montant_credit = ecriture[4]
        montant_debit = ecriture[5]
        id = ecriture[0]
        categorie = ecriture[6]
        if categorie == None:
            print('Date:', date_operation, 'libéllé:', libelle, 'montant crédit:', montant_credit, 'montant débit:', montant_debit)
            choix = input('souhaitez-vous définir une catégorie pour cette ligne de compte? (y/n ou q pour quitter)')
            if choix=='y':
                print('ok on va affecter une categorie')
                categ = input('ok, entrez une categorie parmi les categories existante: ')
                #if is_a_category(categ):
                #    assigner_categorie(id, categ)
                while not is_a_category(categ):
                    print('not a category try again!')
                    categ = input('ok, entrez une categorie parmi les categories existante: ')
                assigner_categorie(id, categ)
            elif choix=='q':
                break
        
def fullauto_parser():
    print('## Full automatic mode ##')
    
    print('## 1. Clean the database ##')
    init_db()

    print('## 2. Fill the database with Cerveau, Categories & Comptes data ##')
    charger_cerveau(Glob.INPUT_BRAIN_FILE)
    charger_categories(Glob.INPUT_CATEGORY_FILE)
    charger_comptes(Glob.INPUT_STATEMENT_FILE)

    print('## 3. Launch the parser ##')
    parser_comptes()

    print('## 4. Backup the parsed data ##')
    sauvegarder_comptes(Glob.OUTPUT_STATEMENT_FILE)

def main():
    print('Welcome in Kontabb')

    # Configuration des arguments et mode
    curs = conn.cursor()
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        '--init',
        '-i',
        default=False,
        help='avec cet argument on lance une réinitialisation de la db',
        action='store_true'
    )
    
    parser.add_argument(
        '--showcomptes',
        default=False,
        help='avec cet argument on voit la lite des ecriture du compte',
        action='store_true'
    )

    parser.add_argument(
        '--showcategories',
        default=False,
        help='avec cet argument on voit la lite des categories',
        action='store_true'
    )
    
    parser.add_argument(
        '--showcerveau',
        default=False,
        help='avec cet argument on voit la liste des souvenirs',
        action='store_true'
    )

    parser.add_argument(
        '--loadcategories',
        default=False,
        help='avec cet argument on charge le fichier csv des categories',
        action='store_true'
    )
    
    parser.add_argument(
        '--loadcomptes',
        default=False,
        help='avec cet argument on charge le fichier csv des comptes',
        action='store_true'
    )
    parser.add_argument(
        '--loadcerveau',
        default=False,
        help='avec cet argument on charge le fichier csv dans cerveau',
        action='store_true'
    )

    parser.add_argument(
        '--savecompte',
        default=False,
        help='avec cet argument on sauvegarde la table compte dans un fichier csv',
        action='store_true'
    )
    parser.add_argument(
        '--savecategories',
        default=False,
        help='avec cet argument on sauvegarde la table categorie dans un fichier csv',
        action='store_true'
    )
    parser.add_argument(
        '--savecerveau',
        default=False,
        help='avec cet argument on sauvegarde la table cerveau dans un fichier csv',
        action='store_true'
    )
    parser.add_argument(
        '--parser',
        default=False,
        help='avec cet argument on parse la table compte et on lui applique les regles de cerveau',
        action='store_true'
    )
    parser.add_argument(
        '--vidertables',
        default=False,
        help='avec cet argument on vide toutes les tables',
        action='store_true'
    )
    parser.add_argument(
        '--manualparser',
        default=False,
        help='avec cet argument on parse manuellement les écritures',
        action='store_true'
    )
    parser.add_argument(
        '--fullautoparser',
        default=False,
        help='avec cet argument on initialise la base, on la charge avec les fichiers de configuration, on lance le parsing auto, et on sauvegarde le résultat',
        action='store_true'
    )

    args = parser.parse_args()

    if args.init:
        init_db()
    
    if args.showcomptes:
        db.show_table('comptes')
    
    if args.showcategories:
        db.show_table('categories')
    
    if args.showcerveau:
        db.show_table('cerveau')
    
    if args.loadcategories:
        charger_categories(Glob.INPUT_CATEGORY_FILE)

    if args.loadcomptes:
        charger_comptes(Glob.INPUT_STATEMENT_FILE)
    
    if args.loadcerveau:
        charger_cerveau(Glob.INPUT_BRAIN_FILE)

    if args.savecompte:
        sauvegarder_comptes(Glob.OUTPUT_STATEMENT_FILE)
    
    if args.savecategories:
        sauvegarder_categories(Glob.OUTPUT_CATEGORY_FILE)

    if args.savecerveau:
        sauvegarder_cerveau(Glob.OUTPUT_BRAIN_FILE)

    if args.parser:
        parser_comptes()

    if args.manualparser:
        parser_compte_manuel()
    
    if args.vidertables:
        vider_tables()
    
    if args.fullautoparser:
        fullauto_parser()

    # appels pour test
    #charger_categories()
    #rechercher_categorie('Animaux')
    # verifier_categories_cerveau()
    conn.close()

if __name__ == "__main__":
    main()