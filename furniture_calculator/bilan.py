import furniture_calculator.geometry as g
from furniture_calculator.model import *

from furniture_calculator.meubles.gauche_bas import inventaire_gauche_bas
from furniture_calculator.meubles.gauche_haut import inventaire_gauche_haut
from furniture_calculator.meubles.droite import inventaire_droite

inventaire = Inventaire()

inventaire += inventaire_gauche_bas
inventaire += inventaire_gauche_haut
inventaire += inventaire_droite

inventaire.ecrire_bilan_markdown("bilan.md")
inventaire.ecrire_bilan_excel("bilan.xlsx")

# print(inventaire.bilan())
