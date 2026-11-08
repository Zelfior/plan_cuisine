import warnings
import furniture_calculator.geometry as g
from furniture_calculator.model import *
from furniture_calculator.meubles.gauche_bas import ajouter_base_meuble

LARGEUR_INTERIEURE = (
    g.LARGEUR_STANDARD - 2 * g.EPAISSEUR_PLANCHE
)

meuble_d1 = Meuble(nom="Droite 1")

ajouter_base_meuble(
    meuble_d1,
    profondeur_caisson = g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE,
    hauteur_caisson = g.HAUTEUR_BAS_DROITE - g.MILIEU_DE_COURSE_PIED - g.EPAISSEUR_PLANCHE,
    largeur_interieure = LARGEUR_INTERIEURE,
    avec_fond = True
)

meuble_d1.ajouter(
    PlancheBlanc(
        longueur=g.LARGEUR_STANDARD,
        largeur=g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE,
        compte=1,
        nom="Haut",
        champ=[L1, G1, G2]
    )
)
val = g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE - g.PROFONDEUR_FOND_DE_MEUBLE

assert val > 532 # Profondeur tiroir
warnings.warn(f"Meuble droite 1 a un tiroir de 532mm, profondeur disponible {val} mm")

meuble_d1.ajouter(
    Vis(compte = 6)
)
meuble_d1.ajouter(
    Tourillon(compte = 4)
)

meuble_d2 = meuble_d1.copy()
meuble_d2.rename("Droite 2")

meuble_d1.ajouter(
    TiroirBas(compte=2)
)
meuble_d1.ajouter(
    TiroirMoyen(compte=2)
)

hauteur_tiroir_bas = (
    g.HAUTEUR_FACADE_BAS_DROITE_CORRIGEE
    - g.INCERTITUDE_SOL
    - g.HAUTEUR_PORTE_KICK_TOE
    - 2 * g.HAUTEUR_TIROIR_MIN
    - g.MARGE_ENTRE_PLANCHE_FACADE * 4
) / 2

meuble_d1.ajouter(
    PlancheVert(
        longueur = g.LARGEUR_STANDARD - g.MARGE_ENTRE_PLANCHE_FACADE*2/3,
        largeur = hauteur_tiroir_bas,
        compte = 1,
        nom = "Tiroir 1",
        champ = [G1, G2, L1, L2]
    )
)
meuble_d1.ajouter(
    PlancheVert(
        longueur = g.LARGEUR_STANDARD - g.MARGE_ENTRE_PLANCHE_FACADE*2/3,
        largeur = hauteur_tiroir_bas,
        compte = 1,
        nom = "Tiroir 2",
        champ = [G1, G2, L1, L2]
    )
)
meuble_d1.ajouter(
    PlancheVert(
        longueur = g.LARGEUR_STANDARD - g.MARGE_ENTRE_PLANCHE_FACADE*2/3,
        largeur = g.HAUTEUR_TIROIR_MIN,
        compte = 1,
        nom = "Tiroir 3",
        champ = [G1, G2, L1, L2]
    )
)
meuble_d1.ajouter(
    PlancheVert(
        longueur = g.LARGEUR_STANDARD - g.MARGE_ENTRE_PLANCHE_FACADE*2/3,
        largeur = g.HAUTEUR_TIROIR_MIN,
        compte = 1,
        nom = "Tiroir 4",
        champ = [G1, G2, L1, L2]
    )
)
meuble_d1.ajouter(
    PlancheFond(
        longueur = LARGEUR_INTERIEURE + 2 * g.LARGEUR_RAINURE_FOND,
        largeur = (
            g.HAUTEUR_BAS_DROITE - g.INCERTITUDE_SOL - g.HAUTEUR_PORTE_KICK_TOE - 2 * g.EPAISSEUR_PLANCHE + g.LARGEUR_RAINURE_FOND
        ),
        compte = 1,
        nom = "Fond"
    )
)

hauteur_tiroir_d2 = (
    g.HAUTEUR_FACADE_BAS_DROITE_CORRIGEE
    - g.INCERTITUDE_SOL
    - g.HAUTEUR_PORTE_KICK_TOE
    - g.HAUTEUR_FOUR
    - g.MARGE_ENTRE_PLANCHE_FACADE * 2
)
meuble_d2.ajouter(
    PlancheVert(
        longueur = g.LARGEUR_STANDARD - g.MARGE_ENTRE_PLANCHE_FACADE*2/3,
        largeur = g.HAUTEUR_FOUR - g.MARGE_ENTRE_PLANCHE_FACADE + g.EPAISSEUR_PLANCHE,
        compte = 1,
        nom = "Porte four",
        champ = [G1, G2, L1, L2]
    )
)
meuble_d2.ajouter(
    PlancheVert(
        longueur = g.LARGEUR_STANDARD - g.MARGE_ENTRE_PLANCHE_FACADE*2/3,
        largeur = hauteur_tiroir_d2,
        compte = 1,
        nom = "Tiroir",
        champ = [G1, G2, L1, L2]
    )
)
meuble_d2.ajouter(
    CharnierePorte(compte = (
        2 * 2
    ))
)
meuble_d2.ajouter(
    PlancheFond(
        longueur = LARGEUR_INTERIEURE + 2 * g.LARGEUR_RAINURE_FOND,
        largeur = (
            g.HAUTEUR_FOUR - g.EPAISSEUR_PLANCHE + g.LARGEUR_RAINURE_FOND
        ),
        compte = 1,
        nom = "Fond"
    )
)








meuble_d3 = Meuble(nom="Droite 3")
meuble_d3.ajouter(
    PlancheVert(
        longueur = g.LARGEUR_STANDARD - g.MARGE_ENTRE_PLANCHE_FACADE*2/3,
        largeur = g.HAUTEUR_MEUBLE_TRAVAIL_DROITE - 2 * g.MARGE_ENTRE_PLANCHE_FACADE - 2 * g.EPAISSEUR_PLANCHE, # on compte marge en haut et en bas
        compte = 2,
        nom = "Porte",
        champ = [G1, G2, L1, L2]
    )
)
meuble_d3.ajouter(
    PlancheBlanc(
        longueur = g.LARGEUR_STANDARD * 2,
        largeur = g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE,
        compte = 1,
        nom = "Bas",
        champ = [L1, G1, G2]
    )
)
meuble_d3.ajouter(
    PlancheBlanc(
        longueur = g.LARGEUR_STANDARD * 2,
        largeur = g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE,
        compte = 1,
        nom = "Haut",
        champ = [L1, G1, G2]
    )
)
meuble_d3.ajouter(
    PlancheBlanc(
        longueur = g.HAUTEUR_MEUBLE_TRAVAIL_DROITE - 2 * g.EPAISSEUR_PLANCHE,
        largeur = g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE,
        compte = 2,
        nom = "Côté extérieurs",
        champ = [L1]
    )
)
meuble_d3.ajouter(
    PlancheBlanc(
        longueur = g.HAUTEUR_MEUBLE_TRAVAIL_DROITE - 2 * g.EPAISSEUR_PLANCHE,
        largeur = g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE,
        compte = 2,
        nom = "Côté intérieurs",
        champ = [L1]
    )
)
meuble_d3.ajouter(
    PlancheBlanc(
        longueur = g.LARGEUR_STANDARD * 2 - 2*(g.EPAISSEUR_PLANCHE * 2 + g.MARGE_PORTE_COULISSANTE),
        largeur = g.LARGEUR_ETAGERE_MEUBLE_TRAVAIL_DROITE,
        compte = 1,
        nom = "Etagere",
        champ = [L1]
    )
)
meuble_d3.ajouter(
    PlancheFond(
        longueur = g.LARGEUR_STANDARD * 2 - 2*(g.EPAISSEUR_PLANCHE * 2 + g.MARGE_PORTE_COULISSANTE) + 2 * g.LARGEUR_RAINURE_FOND,
        largeur = (
            g.HAUTEUR_MEUBLE_TRAVAIL_DROITE - 2 * g.EPAISSEUR_PLANCHE + g.LARGEUR_RAINURE_FOND * 2
        ),
        compte = 1,
        nom = "Fond"
    )
)
meuble_d3.ajouter(
    Vis(compte = (
        6 # extreme gauche
        + 6 # gauche
        + 6 # droite
        + 6 # extreme droite
    ))
)
meuble_d3.ajouter(
    Tourillon(compte = (
        4 # extreme gauche
        + 4 # gauche
        + 4 # droite
        + 4 # extreme droite
    ))
)
meuble_d3.ajouter(
    PionSupportEtagere(compte = (
        8
    ))
)
meuble_d3.ajouter(
    GlissierePorte(compte = (
        2 * 2
    ))
)
meuble_d3.ajouter(
    CharnierePorte(compte = (
        2 * 2
    ))
)



















meuble_d4 = Meuble(nom="Droite 4")

meuble_d4.ajouter(
    PlancheVert(
        longueur=g.HAUTEUR_DROITE - g.HAUTEUR_BAS_DROITE - g.HAUTEUR_MEUBLE_TRAVAIL_DROITE,
        largeur=g.LARGEUR_STANDARD- g.MARGE_ENTRE_PLANCHE_FACADE*2/3,
        compte=1,
        nom="Porte",
        champ=[L1, L2, G1, G2]
    )
)

meuble_d4.ajouter(
    PlancheBlanc(
        longueur=g.LARGEUR_STANDARD,
        largeur=g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE,
        compte=1,
        nom="Bas",
        champ=[L1, G1, G2]
    )
)
meuble_d4.ajouter(
    PlancheBlanc(
        longueur=g.LARGEUR_STANDARD,
        largeur=g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE,
        compte=1,
        nom="Haut",
        champ=[L1, G1, G2]
    )
)
meuble_d4.ajouter(
    PlancheBlanc(
        longueur=g.HAUTEUR_DROITE - g.HAUTEUR_BAS_DROITE - g.HAUTEUR_MEUBLE_TRAVAIL_DROITE - 2 * g.EPAISSEUR_PLANCHE,
        largeur=g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE,
        compte=1,
        nom="Gauche",
        champ=[L1]
    )
)
meuble_d4.ajouter(
    PlancheBlanc(
        longueur=g.HAUTEUR_DROITE - g.HAUTEUR_BAS_DROITE - g.HAUTEUR_MEUBLE_TRAVAIL_DROITE - 2 * g.EPAISSEUR_PLANCHE,
        largeur=g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE,
        compte=1,
        nom="DROITE",
        champ=[L1]
    )
)
meuble_d4.ajouter(
    PlancheBlanc(
        longueur=g.LARGEUR_STANDARD - 2*g.EPAISSEUR_PLANCHE,
        largeur=g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE - g.MARGE_DEVANT_ETAGERE - g.PROFONDEUR_FOND_DE_MEUBLE,
        compte=2,
        nom="Etagere",
        champ=[L1]
    )
)
meuble_d4.ajouter(
    PlancheFond(
        longueur = g.LARGEUR_STANDARD - 2*g.EPAISSEUR_PLANCHE + 2 * g.LARGEUR_RAINURE_FOND,
        largeur = (
            g.HAUTEUR_DROITE - g.HAUTEUR_BAS_DROITE - g.HAUTEUR_MEUBLE_TRAVAIL_DROITE - 2 * g.EPAISSEUR_PLANCHE + g.LARGEUR_RAINURE_FOND * 2
        ),
        compte = 1,
        nom = "Fond"
    )
)

meuble_d4.ajouter(
    PionSupportEtagere(compte = (
        8
    ))
)
meuble_d4.ajouter(
    Vis(compte = (
        6 # gauche
        + 6 # droite
    ))
)
meuble_d4.ajouter(
    Tourillon(compte = (
        4 # gauche
        + 4 # droite
    ))
)
meuble_d4.ajouter(
    CharnierePorte(compte = (
        2
    ))
)

meuble_d5 = meuble_d4.copy()
meuble_d5.rename("Droite 5")


















meuble_d6 = Meuble(nom="Droite 6")




meuble_d6.ajouter(
    PlancheVert(
        longueur=g.HAUTEUR_DROITE - g.HAUTEUR_SUR_FRIGO,
        largeur=g.LARGEUR_STANDARD- g.MARGE_ENTRE_PLANCHE_FACADE*2/3,
        compte=1,
        nom="Porte",
        champ=[L1, L2, G1, G2]
    )
)

meuble_d6.ajouter(
    PlancheBlanc(
        longueur=g.LARGEUR_STANDARD,
        largeur=g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE,
        compte=1,
        nom="Bas",
        champ=[L1, G1, G2]
    )
)
meuble_d6.ajouter(
    PlancheBlanc(
        longueur=g.LARGEUR_STANDARD,
        largeur=g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE,
        compte=1,
        nom="Haut",
        champ=[L1, G1, G2]
    )
)
meuble_d6.ajouter(
    PlancheBlanc(
        longueur=g.HAUTEUR_DROITE - g.HAUTEUR_SUR_FRIGO - 2*g.EPAISSEUR_PLANCHE,
        largeur=g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE,
        compte=1,
        nom="Gauche",
        champ=[L1]
    )
)
meuble_d6.ajouter(
    PlancheBlanc(
        longueur=g.HAUTEUR_DROITE - g.HAUTEUR_SUR_FRIGO - 2*g.EPAISSEUR_PLANCHE,
        largeur=g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE,
        compte=1,
        nom="DROITE",
        champ=[L1]
    )
)
meuble_d6.ajouter(
    PlancheBlanc(
        longueur=g.LARGEUR_STANDARD - 2*g.EPAISSEUR_PLANCHE,
        largeur=g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE - g.MARGE_DEVANT_ETAGERE - g.PROFONDEUR_FOND_DE_MEUBLE,
        compte=2,
        nom="Etagere",
        champ=[L1]
    )
)
meuble_d4.ajouter(
    PlancheFond(
        longueur = g.LARGEUR_STANDARD - 2*g.EPAISSEUR_PLANCHE + 2 * g.LARGEUR_RAINURE_FOND,
        largeur = (
            g.HAUTEUR_DROITE - g.HAUTEUR_SUR_FRIGO - 2*g.EPAISSEUR_PLANCHE + g.LARGEUR_RAINURE_FOND * 2
        ),
        compte = 1,
        nom = "Fond"
    )
)


meuble_d6.ajouter(
    PionSupportEtagere(compte = (
        8
    ))
)
meuble_d6.ajouter(
    Vis(compte = (
        6 # gauche
        + 6 # droite
    ))
)
meuble_d6.ajouter(
    Tourillon(compte = (
        4 # gauche
        + 4 # droite
    ))
)
meuble_d6.ajouter(
    CharnierePorte(compte = (
        2
    ))
)















inventaire_droite = Inventaire()

inventaire_droite.ajouter(meuble_d1)
inventaire_droite.ajouter(meuble_d2)
inventaire_droite.ajouter(meuble_d3)
inventaire_droite.ajouter(meuble_d4)
inventaire_droite.ajouter(meuble_d5)
inventaire_droite.ajouter(meuble_d6)
