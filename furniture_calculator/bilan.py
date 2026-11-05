import furniture_calculator.geometry as g
from furniture_calculator.model import *

from furniture_calculator.meubles.gauche_bas import inventaire_gauche_bas
from furniture_calculator.meubles.gauche_haut import inventaire_gauche_haut
from furniture_calculator.meubles.droite import meuble_d1, meuble_d2, meuble_d3, meuble_d4

inventaire = Inventaire()

inventaire += inventaire_gauche_bas
inventaire += inventaire_gauche_haut

inventaire.ecrire_bilan_markdown("bilan.md")

print(inventaire.bilan())
