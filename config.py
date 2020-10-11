# coding: utf-8

print("import du module config")

class Glob:
    DB_PATH='kontab.db'
    INPUT_BRAIN_FILE='input_cerveau.csv'
    INPUT_STATEMENT_FILE='comptes_mois_N.csv'
    INPUT_CATEGORY_FILE='categories_mois_N.csv'
    OUTPUT_STATEMENT_FILE='resultat_comptes_mois_N.csv'
    OUTPUT_CATEGORY_FILE='backup_catergoy.csv'
    OUTPUT_BRAIN_FILE='backup_brain.csv'

    # database structure
    dicoT={"cerveau":[('id_cerv','k',"primary key"),
                        ('libelle',30,"name"),
                        ('categorie',30,"associated category")],
            "categories":[('id_categ','k',"primary key"),
                        ('nom', 30, "name of the category"),
                        ('categ_parent', 30, "parent category")],
            "comptes":[('id_compt','k',"primary key"),
                        ('date_operation',30, "operation date"),
                        ('date_valeur', 30, "value date"),
                        ('libelle',200, "description"),
                        ('montant_credit','f', "montant crédit"),
                        ('montant_debit','f', "montant débit"),
                        ('categorie',30, "associated category")]}
