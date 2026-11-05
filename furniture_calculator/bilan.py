import geometry as g
from model import *

from meubles.gauche_bas import meuble_g1, meuble_g2, meuble_g3, kick_drawer
from meubles.gauche_haut import meuble_g4, meuble_g5, meuble_g6
from meubles.droite import meuble_d1, meuble_d2, meuble_d3, meuble_d4

inventaire = Inventaire()
inventaire.ajouter(meuble_g1)
inventaire.ajouter(meuble_g2)
inventaire.ajouter(meuble_g3)
inventaire.ajouter(meuble_g4)
inventaire.ajouter(meuble_g5)
inventaire.ajouter(meuble_g6)
inventaire.ajouter(meuble_d1)
inventaire.ajouter(meuble_d2)
inventaire.ajouter(meuble_d3)
inventaire.ajouter(meuble_d4)


for name in [
    "kick_drawer_g1",
    "kick_drawer_g2",
    "kick_drawer_g3",
    "kick_drawer_d1",
    "kick_drawer_d2",
]:
    kd = kick_drawer.copy()
    kd.rename(name)
    inventaire.ajouter(kd)

inventaire.ecrire_bilan_markdown("bilan.md")

print(inventaire.bilan())
