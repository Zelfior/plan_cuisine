import geometry as g
from model import *


#  _          _
# | |        | |
# | |        | |
# | |        | |
# | |        | |
# | |________| |
# | |________| |
# |_|        |_|
meuble_g1 = Meuble(nom="Gauche 1")
meuble_g1.ajouter(
    PlancheBlanc(
        longueur = g.PROFONDEUR_GAUCHE_BAS - g.EPAISSEUR_PLANCHE,
        largeur = g.HAUTEUR_SOUS_PLAN_GAUCHE - g.MILIEU_DE_COURSE_PIED,
        compte = 2
    )
)
meuble_g1.ajouter(
    PlancheBlanc(
        longueur = g.PROFONDEUR_GAUCHE_BAS - g.EPAISSEUR_PLANCHE,
        largeur = g.LARGEUR_STANDARD - 2 * g.EPAISSEUR_PLANCHE,
        compte = 1
    )
)
meuble_g1.ajouter(
    PlancheVert(
        longueur = (
            g.HAUTEUR_SOUS_PLAN_GAUCHE
            - g.INCERTITUDE_SOL
            - g.HAUTEUR_PORTE_KICK_TOE
            - g.MARGE_ENTRE_PLANCHE_FACADE
        ),
        largeur = g.LARGEUR_STANDARD - g.MARGE_ENTRE_PLANCHE_FACADE,
        compte = 1
    )
)
meuble_g1.ajouter(
    Vis(
        compte = 6
    )
)
meuble_g1.ajouter(
    Tourillon(
        compte = 4
    )
)
meuble_g1.ajouter(
    CharnierePorte(
        compte = 2
    )
)
meuble_g1.ajouter(
    PlancheFond(
        longueur = (
            g.HAUTEUR_SOUS_PLAN_GAUCHE
            - g.INCERTITUDE_SOL
            - g.HAUTEUR_PORTE_KICK_TOE
            - g.EPAISSEUR_PLANCHE
            + g.LARGEUR_RAINURE_FOND
        ),
        largeur = g.LARGEUR_STANDARD - 2 * g.EPAISSEUR_PLANCHE + 2 * g.LARGEUR_RAINURE_FOND,
        compte = 1
    )
)

#  _          _
# | |        | |
# | |________| |
# | |________| |
# | |        | |
# | |________| |
# | |________| |
# |_|        |_|
meuble_g2 = meuble_g1.copy()
meuble_g2.rename("Gauche 2")

meuble_g2.ajouter(
    PlancheBlanc(
        longueur = (
            g.PROFONDEUR_GAUCHE_BAS
            - g.MARGE_DEVANT_ETAGERE
            - g.EPAISSEUR_PLANCHE
            - g.PROFONDEUR_FOND_DE_MEUBLE
        ),
        largeur = g.LARGEUR_STANDARD - 2 * g.EPAISSEUR_PLANCHE,
        compte = 1
    )
)
meuble_g2.ajouter(
    PionSupportEtagere(
        compte = 4
    )
)

#  _          _
# | |        | |
# | |        | |
# | |        | |
# | |        | |
# | |________| |
# | |________| |
# |_|        |_|

meuble_g3 = Meuble(nom="Gauche 3")
meuble_g3.ajouter(
    PlancheBlanc(
        longueur = g.PROFONDEUR_GAUCHE_BAS - g.EPAISSEUR_PLANCHE,
        largeur = g.HAUTEUR_SOUS_PLAN_GAUCHE - g.MILIEU_DE_COURSE_PIED,
        compte = 2
    )
)
meuble_g3.ajouter(
    PlancheBlanc(
        longueur = g.PROFONDEUR_GAUCHE_BAS - g.EPAISSEUR_PLANCHE,
        largeur = g.LARGEUR_STANDARD - 2 * g.EPAISSEUR_PLANCHE,
        compte = 1
    )
)
meuble_g3.ajouter(
    Vis(
        compte = 6
    )
)
meuble_g3.ajouter(
    Tourillon(
        compte = 4
    )
)
meuble_g3.ajouter(
    PlancheFond(
        longueur = (
            g.HAUTEUR_SOUS_PLAN_GAUCHE
            - g.INCERTITUDE_SOL
            - g.HAUTEUR_PORTE_KICK_TOE
            - g.EPAISSEUR_PLANCHE
            + g.LARGEUR_RAINURE_FOND
        ),
        largeur = g.LARGEUR_STANDARD - 2 * g.EPAISSEUR_PLANCHE + 2 * g.LARGEUR_RAINURE_FOND,
        compte = 1
    )
)
meuble_g3.ajouter(
    TiroirBas(compte=2)
)
meuble_g3.ajouter(
    TiroirMoyen(compte=2)
)
meuble_g3.ajouter(
    PlancheVert(
        longueur = (
            g.HAUTEUR_TIROIR_MIN
        ),
        largeur = g.LARGEUR_STANDARD - g.MARGE_ENTRE_PLANCHE_FACADE,
        compte = 2
    )
)
meuble_g3.ajouter(
    PlancheVert(
        longueur = (
            g.HAUTEUR_SOUS_PLAN_GAUCHE
            - g.INCERTITUDE_SOL
            - g.HAUTEUR_PORTE_KICK_TOE
            - g.MARGE_ENTRE_PLANCHE_FACADE
            - g.HAUTEUR_TIROIR_MIN * 2
            - 28
            - 3 * g.MARGE_ENTRE_PLANCHE_FACADE
        ),
        largeur = g.LARGEUR_STANDARD - g.MARGE_ENTRE_PLANCHE_FACADE,
        compte = 2
    )
)
meuble_g3.ajouter(
    PlancheVert(
        longueur = (
            28
        ),
        largeur = g.LARGEUR_STANDARD - g.MARGE_ENTRE_PLANCHE_FACADE,
        compte = 2
    )
)

# To be refined
kick_drawer = Meuble(nom="Kick Drawer")
kick_drawer.ajouter(
    PlancheVert(
        longueur = (
            g.HAUTEUR_PORTE_KICK_TOE
        ),
        largeur = g.LARGEUR_STANDARD - g.MARGE_ENTRE_PLANCHE_FACADE,
        compte = 1
    )
)
kick_drawer.ajouter(
    RailKickToe(compte=2)
)
kick_drawer.ajouter(
    Vis(compte=2*(2+2+1+1))
)
kick_drawer.ajouter(
    Tourillon(compte=2*5)
)
kick_drawer.ajouter(
    PlancheBlanc(
        longueur = g.PROFONDEUR_KICK_TOE,
        largeur = g.LARGEUR_KICK_TOE,
        compte = 1
    )
)



inventaire = Inventaire()
inventaire.ajouter(meuble_g1)
inventaire.ajouter(meuble_g2)
inventaire.ajouter(meuble_g3)
inventaire.ajouter(kick_drawer)
inventaire.ecrire_bilan_markdown("bilan.md")

print(inventaire.bilan())
