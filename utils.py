# coding: utf-8

print("import du module utils")

def get_table_list(cursor):
    _SQL = """SELECT name FROM sqlite_master
    WHERE type='table'
    ORDER BY name"""
    cursor.execute(_SQL)
    results = cursor.fetchall()
    table_list = [
        v[0] for v in results
        if v[0] != "sqlite_sequence"
    ]
    print("voici toutes les tables:", table_list)
    return table_list

def delete_table(cursor, table):
    # suppression de la table
    cursor.execute("DROP TABLE " +table+"")
    print ("table ", table, "supprimée")

def delete_all_tables(cursor):
    table_list = get_table_list(cursor)

    for table in table_list:
        delete_table(cursor, table)
    print('Tables supprimées')

def show_table(cursor, table):
    cursor.execute("SELECT * from "+table+"")
    for line in cursor.fetchall():
        print(line)

def clean_table(cursor, table):
    cursor.execute("DELETE FROM " +table+"")
    print ("table ", table, "vidée")

def clean_all_tables(cursor):
    table_list = get_table_list(cursor)
    for table in table_list:
        clean_table(cursor, table)



    
