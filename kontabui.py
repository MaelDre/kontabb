#import Tkinter as tk
import PySimpleGUI as sg
from config import Glob
import kontab as kt


# UI
# Définition des éléments de le fenêtre
layout = [  [sg.Text("Bienvenue dans Kontab")],
            # [sg.Input()],
            [sg.Text("La configuration actuelle est la suivante :")],
            [sg.Text("fichier Cerveau des opérations connues :"), sg.Text(Glob.INPUT_BRAIN_FILE)],
            [sg.Text("Liste des catégories :"), sg.Text(Glob.INPUT_CATEGORY_FILE)],
            [sg.Text("Fichier de compte d'entrée :"), sg.Text(Glob.INPUT_STATEMENT_FILE)],
            [sg.Text("Fichier résultat de compte analysé :"), sg.Text(Glob.OUTPUT_STATEMENT_FILE)],
            [sg.Button('Lancer')],
            [sg.Button('Quitter')] ]

# Création de la fenêtre
window = sg.Window('Kontab - Analyse auto de comptes', layout)

# Affichage et interaction avec le fenêtre
# Event loop or Window.read call

# Boucle d'évènements
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button, Do something with the information gathered
    if event == "Quitter" or event == sg.WIN_CLOSED:
        print('Bye! Thanks for using Kontab')
        break
    if event == "Lancer":
        kt.fullauto_parser()

# Fin de l'application et fermeture de la fenêtre
window.close()