import furniture_calculator.geometry as g
from furniture_calculator.model import *



meuble_g4 = Meuble(nom="Gauche 4")

meuble_g4.ajouter(
    PlancheBlanc(
        longueur = g.PROFONDEUR_MEUBLE_GAUCHE_HAUT - g.EPAISSEUR_PLANCHE,
        largeur = g.HAUTEUR_HAUT_GAUCHE,
        compte = 1,
        nom = "Côté gauche"
    )
)
meuble_g4.ajouter(
    PlancheBlanc(
        longueur = g.PROFONDEUR_MEUBLE_GAUCHE_HAUT - g.EPAISSEUR_PLANCHE,
        largeur = g.HAUTEUR_HAUT_GAUCHE,
        compte = 1,
        nom = "Côté droite"
    )
)
meuble_g4.ajouter(
    PlancheBlanc(
        longueur = g.PROFONDEUR_MEUBLE_GAUCHE_HAUT - g.EPAISSEUR_PLANCHE,
        largeur = g.LARGEUR_STANDARD - 2 * g.EPAISSEUR_PLANCHE,
        compte = 1,
        nom = "Bas"
    )
)
meuble_g4.ajouter(
    PlancheBlanc(
        longueur = g.PROFONDEUR_MEUBLE_GAUCHE_HAUT - g.EPAISSEUR_PLANCHE,
        largeur = g.LARGEUR_STANDARD - 2 * g.EPAISSEUR_PLANCHE,
        compte = 1,
        nom = "Haut"
    )
)
meuble_g4.ajouter(
    PlancheVert(
        longueur = g.HAUTEUR_HAUT_GAUCHE,
        largeur = g.LARGEUR_STANDARD - g.MARGE_ENTRE_PLANCHE_FACADE,
        compte = 1,
        nom = "Porte"
    )
)
meuble_g4.ajouter(
    PlancheFond(
        longueur = g.HAUTEUR_HAUT_GAUCHE - 2 * (g.EPAISSEUR_PLANCHE - g.PROFONDEUR_RAINURE_FOND),
        largeur = g.LARGEUR_STANDARD - 2 * (g.EPAISSEUR_PLANCHE - g.PROFONDEUR_RAINURE_FOND),
        compte = 1,
        nom = "Fond"
    )
)
meuble_g4.ajouter(
    PlancheBlanc(
        longueur = g.PROFONDEUR_MEUBLE_GAUCHE_HAUT - g.EPAISSEUR_PLANCHE - g.MARGE_DEVANT_ETAGERE - g.PROFONDEUR_FOND_DE_MEUBLE,
        largeur = g.LARGEUR_STANDARD - 2 * g.EPAISSEUR_PLANCHE,
        compte = 2,
        nom = "Etagère"
    )
)
meuble_g4.ajouter(
    Vis(
        compte = 12
    )
)
meuble_g4.ajouter(
    Tourillon(
        compte = 8
    )
)
meuble_g4.ajouter(
    CharnierePorte(
        compte = 2
    )
)
meuble_g4.ajouter(
    PionSupportEtagere(
        compte = 8
    )
)

meuble_g5 = meuble_g4.copy()
meuble_g5.rename("Gauche 5")

meuble_g6 = Meuble(nom="Gauche 6")


inventaire_gauche_haut = Inventaire()

inventaire_gauche_haut.ajouter(meuble_g4)
inventaire_gauche_haut.ajouter(meuble_g5)
inventaire_gauche_haut.ajouter(meuble_g6)
