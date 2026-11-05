import geometry as g
from model import *

meuble_d1 = Meuble(nom="Droite 1")
meuble_d2 = Meuble(nom="Droite 2")
meuble_d3 = Meuble(nom="Droite 3")
meuble_d4 = Meuble(nom="Droite 4")

meuble_d1.ajouter(
    PlancheBlanc(
        longueur = g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE,
        largeur = g.HAUTEUR_BAS_DROITE - g.INCERTITUDE_SOL - g.HAUTEUR_PORTE_KICK_TOE,
        compte = 1,
        nom = "Côtés gauche"
    )
)
meuble_d1.ajouter(
    PlancheBlanc(
        longueur = g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE,
        largeur = g.HAUTEUR_BAS_DROITE - g.INCERTITUDE_SOL - g.HAUTEUR_PORTE_KICK_TOE,
        compte = 1,
        nom = "Côtés droite"
    )
)
meuble_d1.ajouter(
    PlancheBlanc(
        longueur = g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE,
        largeur = g.LARGEUR_STANDARD - 2 * g.EPAISSEUR_PLANCHE,
        compte = 1,
        nom = "Base"
    )
)
meuble_d1.ajouter(
    PlancheBlanc(
        longueur = g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE - g.MARGE_DEVANT_ETAGERE - g.PROFONDEUR_FOND_DE_MEUBLE,
        largeur = g.LARGEUR_STANDARD - 2 * g.EPAISSEUR_PLANCHE,
        compte = 1,
        nom = "Etagère"
    )
)
meuble_d1.ajouter(
    TiroirBas(compte=1)
)

meuble_d2.ajouter(
    PlancheBlanc(
        longueur = g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE,
        largeur = g.HAUTEUR_BAS_DROITE - g.INCERTITUDE_SOL - g.HAUTEUR_PORTE_KICK_TOE,
        compte = 1,
        nom = "Côtés gauche"
    )
)
meuble_d2.ajouter(
    PlancheBlanc(
        longueur = g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE,
        largeur = g.HAUTEUR_BAS_DROITE - g.INCERTITUDE_SOL - g.HAUTEUR_PORTE_KICK_TOE,
        compte = 1,
        nom = "Côtés droite"
    )
)
meuble_d2.ajouter(
    TiroirBas(compte=1)
)
