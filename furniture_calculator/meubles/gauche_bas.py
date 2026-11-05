import furniture_calculator.geometry as g
from furniture_calculator.model import *


# ============================================================
# DIMENSIONS COMMUNES
# ============================================================

LARGEUR_INTERIEURE = (
    g.LARGEUR_STANDARD - 2 * g.EPAISSEUR_PLANCHE
)

HAUTEUR_CAISSON = (
    g.HAUTEUR_SOUS_PLAN_GAUCHE - g.MILIEU_DE_COURSE_PIED
)

PROFONDEUR_CAISSON = (
    g.PROFONDEUR_MEUBLE_GAUCHE_BAS
    - g.EPAISSEUR_PLANCHE
    - g.MARGE_ARRIERE_GAUCHE_BAS
)

PROFONDEUR_CAISSON_EVIER = (
    g.PROFONDEUR_MEUBLE_GAUCHE_BAS
    - g.EPAISSEUR_PLANCHE
    - g.PROFONDEUR_VIDE_SANITAIRE_EVIER
)


# ============================================================
# STRUCTURE COMMUNE
# ============================================================

def ajouter_base_meuble(
    meuble: Meuble,
    profondeur_caisson: float = PROFONDEUR_CAISSON,
    hauteur_caisson: float = HAUTEUR_CAISSON,
    largeur_interieure: float = LARGEUR_INTERIEURE,
    avec_fond: bool = True
):
    """Ajoute à un meuble les trois planches de base

    Parameters
    ----------
    meuble : Meuble
        Meuble auquel ajouter les planches de base
    profondeur_caisson : float, optional
        Profondeur du caisson, by default PROFONDEUR_CAISSON
    hauteur_caisson : float, optional
        Hauteur du caisson, by default HAUTEUR_CAISSON
    largeur_interieure : float, optional
        Largeur intérieure du meuble, by default LARGEUR_INTERIEURE
    avec_fond : bool, optional
        Indique si le meuble doit avoir un fond ou non, by default True
    """
    meuble.ajouter(
        PlancheBlanc(
            longueur=profondeur_caisson,
            largeur=hauteur_caisson,
            compte=1,
            nom="Côtés gauche"
        )
    )

    meuble.ajouter(
        PlancheBlanc(
            longueur=profondeur_caisson,
            largeur=hauteur_caisson,
            compte=1,
            nom="Côtés droite"
        )
    )

    meuble.ajouter(
        PlancheBlanc(
            longueur=profondeur_caisson,
            largeur=largeur_interieure,
            compte=1,
            nom="Base"
        )
    )

    meuble.ajouter(Vis(compte=6))
    meuble.ajouter(Tourillon(compte=4))

    if avec_fond:
        meuble.ajouter(
            PlancheFond(
                longueur=(
                    g.HAUTEUR_SOUS_PLAN_GAUCHE
                    - g.HAUTEUR_DEBUT_MEUBLE_BAS
                    - g.EPAISSEUR_PLANCHE
                    + 2 * g.LARGEUR_RAINURE_FOND
                ),
                largeur=largeur_interieure + 2 * g.LARGEUR_RAINURE_FOND,
                compte=1,
                nom="Fond"
            )
        )


# ============================================================
# GAUCHE 1
# ============================================================

meuble_g1 = Meuble(nom="Gauche 1")

"""
#   VERTICAL

-- Plan de travail -- hauteur HAUTEUR_SOUS_PLAN_GAUCHE

-- GAP INTER PLANCHES -- MARGE_ENTRE_PLANCHE_FACADE

Hauteur de porte

-- GAP INTER PLANCHES -- MARGE_ENTRE_PLANCHE_FACADE

Kick-toe (plinthe) -- hauteur HAUTEUR_PORTE_KICK_TOE

-- MARGE SOL -- incertitude de niveau du sol


#   HORIZONTAL

Planche de gauche -- toute la verticale, épaisseur EPAISSEUR_PLANCHE

Contenu Meuble -- largeur LARGEUR_STANDARD - 2 * EPAISSEUR_PLANCHE

Planche de droite -- toute la verticale, épaisseur EPAISSEUR_PLANCHE


#   PROFONDEUR

Façade -- profondeur EPAISSEUR_PLANCHE

Meuble -- profondeur restante dans PROFONDEUR_GAUCHE_BAS
          - EPAISSEUR_PLANCHE
          - PROFONDEUR_VIDE_SANITAIRE_EVIER

Fond -- profondeur PROFONDEUR_FOND_DE_MEUBLE

Vide sanitaire -- PROFONDEUR_VIDE_SANITAIRE
"""

ajouter_base_meuble(meuble_g1, profondeur_caisson=PROFONDEUR_CAISSON_EVIER, avec_fond=False)

meuble_g1.ajouter(
    PlancheBlanc(
        longueur=(
            g.HAUTEUR_FOND_EVIER
        ),
        largeur=LARGEUR_INTERIEURE,
        compte=1,
        nom="Fond"
    )
)

meuble_g1.ajouter(
    PlancheVert(
        longueur=(
            g.HAUTEUR_SOUS_PLAN_GAUCHE
            - g.HAUTEUR_DEBUT_MEUBLE_BAS
            - 2 * g.MARGE_ENTRE_PLANCHE_FACADE
        ),
        largeur=g.LARGEUR_STANDARD - g.MARGE_ENTRE_PLANCHE_FACADE,
        compte=1,
        nom="Porte"
    )
)

meuble_g1.ajouter(CharnierePorte(compte=2))

meuble_g1.ajouter(Vis(compte=4))
meuble_g1.ajouter(Tourillon(compte=4))



# ============================================================
# GAUCHE 2
# ============================================================

meuble_g2 = Meuble(nom="Gauche 2")

"""
#   VERTICAL

-- Plan de travail -- hauteur HAUTEUR_SOUS_PLAN_GAUCHE

-- GAP INTER PLANCHES -- MARGE_ENTRE_PLANCHE_FACADE

Hauteur de porte

-- GAP INTER PLANCHES -- MARGE_ENTRE_PLANCHE_FACADE

Kick-toe (plinthe) -- hauteur HAUTEUR_PORTE_KICK_TOE

-- MARGE SOL -- incertitude de niveau du sol


#   HORIZONTAL

Planche de gauche -- toute la verticale, épaisseur EPAISSEUR_PLANCHE

Contenu Meuble -- largeur LARGEUR_STANDARD - 2 * EPAISSEUR_PLANCHE

Etagère -- largeur LARGEUR_STANDARD - 2 * EPAISSEUR_PLANCHE

Planche de droite -- toute la verticale, épaisseur EPAISSEUR_PLANCHE


#   PROFONDEUR

Façade -- profondeur EPAISSEUR_PLANCHE

Meuble -- profondeur restante dans PROFONDEUR_GAUCHE_BAS
          - EPAISSEUR_PLANCHE
          - PROFONDEUR_VIDE_SANITAIRE

Fond -- profondeur PROFONDEUR_FOND_DE_MEUBLE

Vide sanitaire -- PROFONDEUR_VIDE_SANITAIRE
"""

ajouter_base_meuble(meuble_g2)

meuble_g2.ajouter(
    PlancheBlanc(
        longueur=(
            PROFONDEUR_CAISSON
            - g.MARGE_DEVANT_ETAGERE
            - g.PROFONDEUR_FOND_DE_MEUBLE
        ),
        largeur=LARGEUR_INTERIEURE,
        compte=1,
        nom="Etagère"
    )
)

meuble_g2.ajouter(PionSupportEtagere(compte=4))

meuble_g2.ajouter(
    PlancheVert(
        longueur=(
            g.HAUTEUR_SOUS_PLAN_GAUCHE
            - g.HAUTEUR_DEBUT_MEUBLE_BAS
            - 2 * g.MARGE_ENTRE_PLANCHE_FACADE
        ),
        largeur=g.LARGEUR_STANDARD - g.MARGE_ENTRE_PLANCHE_FACADE,
        compte=1,
        nom="Porte"
    )
)

meuble_g2.ajouter(CharnierePorte(compte=2))


# ============================================================
# GAUCHE 3
# ============================================================

meuble_g3 = Meuble(nom="Gauche 3")

"""
#   VERTICAL

-- Plan de travail -- hauteur HAUTEUR_SOUS_PLAN_GAUCHE

-- GAP INTER PLANCHES -- MARGE_ENTRE_PLANCHE_FACADE

Tiroir minimal - HAUTEUR_TIROIR_MIN

-- GAP INTER PLANCHES -- MARGE_ENTRE_PLANCHE_FACADE

Tiroir minimal - HAUTEUR_TIROIR_MIN

-- GAP INTER PLANCHES -- MARGE_ENTRE_PLANCHE_FACADE

Tiroir reste

-- GAP INTER PLANCHES -- MARGE_ENTRE_PLANCHE_FACADE

Tiroir maximal - 28 cm

-- GAP INTER PLANCHES -- MARGE_ENTRE_PLANCHE_FACADE

Kick-toe (plinthe) -- hauteur HAUTEUR_PORTE_KICK_TOE

-- MARGE SOL -- incertitude de niveau du sol


#   HORIZONTAL

Planche de gauche -- toute la verticale, épaisseur EPAISSEUR_PLANCHE

Contenu Meuble -- largeur LARGEUR_STANDARD - 2 * EPAISSEUR_PLANCHE

Etagère -- largeur LARGEUR_STANDARD - 2 * EPAISSEUR_PLANCHE

Planche de droite -- toute la verticale, épaisseur EPAISSEUR_PLANCHE


#   PROFONDEUR

Façade -- profondeur EPAISSEUR_PLANCHE

Meuble -- profondeur restante dans PROFONDEUR_GAUCHE_BAS
          - EPAISSEUR_PLANCHE
          - PROFONDEUR_FOND_DE_MEUBLE
          - PROFONDEUR_VIDE_SANITAIRE

Fond -- profondeur PROFONDEUR_FOND_DE_MEUBLE

Vide sanitaire -- PROFONDEUR_VIDE_SANITAIRE
"""

ajouter_base_meuble(meuble_g3)

HAUTEUR_TIROIR_MIN = g.HAUTEUR_TIROIR_MIN
HAUTEUR_TIROIR_MAX = 28

NOMBRE_INTERSTICES = 4

HAUTEUR_TIROIR_RESTANT = (
    g.HAUTEUR_SOUS_PLAN_GAUCHE
    - g.HAUTEUR_DEBUT_MEUBLE_BAS
    - g.HAUTEUR_PORTE_KICK_TOE
    - 2 * HAUTEUR_TIROIR_MIN
    - HAUTEUR_TIROIR_MAX
    - NOMBRE_INTERSTICES * g.MARGE_ENTRE_PLANCHE_FACADE
)

meuble_g3.ajouter(TiroirBas(compte=2))
meuble_g3.ajouter(TiroirMoyen(compte=2))

meuble_g3.ajouter(
    PlancheVert(
        longueur=HAUTEUR_TIROIR_MIN,
        largeur=g.LARGEUR_STANDARD - g.MARGE_ENTRE_PLANCHE_FACADE,
        compte=2,
        nom="Porte tiroir bas"
    )
)

meuble_g3.ajouter(
    PlancheVert(
        longueur=HAUTEUR_TIROIR_RESTANT,
        largeur=g.LARGEUR_STANDARD - g.MARGE_ENTRE_PLANCHE_FACADE,
        compte=1,
        nom="Porte tiroir reste"
    )
)

meuble_g3.ajouter(
    PlancheVert(
        longueur=HAUTEUR_TIROIR_MAX,
        largeur=g.LARGEUR_STANDARD - g.MARGE_ENTRE_PLANCHE_FACADE,
        compte=1,
        nom="Porte tiroir haut"
    )
)


# ============================================================
# KICK DRAWER
# ============================================================

# To be refined

def make_kick_drawer(
    name: str = "Kick Drawer",
    profondeur_kick_toe: float = g.PROFONDEUR_KICK_TOE_GAUCHE,
):
    """Kick drawer"""
    kick_drawer = Meuble(nom=name)

    kick_drawer.ajouter(
        PlancheVert(
            longueur=g.HAUTEUR_PORTE_KICK_TOE,
            largeur=g.LARGEUR_STANDARD - g.MARGE_ENTRE_PLANCHE_FACADE,
            compte=1,
            nom="Porte kick-toe"
        )
    )

    kick_drawer.ajouter(RailKickToe(compte=2))

    kick_drawer.ajouter(
        Vis(compte=2 * (2 + 2 + 1 + 1))
    )

    kick_drawer.ajouter(
        Tourillon(compte=2 * 5)
    )

    kick_drawer.ajouter(
        PlancheBlanc(
            longueur=profondeur_kick_toe,
            largeur=g.LARGEUR_KICK_TOE,
            compte=1,
            nom="Base kick-toe"
        )
    )

    kick_drawer.ajouter(
        PlancheBlanc(
            longueur=profondeur_kick_toe,
            largeur=g.HAUTEUR_KICK_TOE,
            compte=1,
            nom="gauche"
        )
    )
    kick_drawer.ajouter(
        PlancheBlanc(
            longueur=profondeur_kick_toe,
            largeur=g.HAUTEUR_KICK_TOE,
            compte=1,
            nom="droite"
        )
    )
    kick_drawer.ajouter(
        PlancheBlanc(
            longueur=g.LARGEUR_KICK_TOE - 2 * g.EPAISSEUR_PLANCHE,
            largeur=g.HAUTEUR_KICK_TOE,
            compte=1,
            nom="fond"
        )
    )

    return kick_drawer

# ============================================================
# INVENTAIRE
# ============================================================

inventaire_gauche_bas = Inventaire()

inventaire_gauche_bas.ajouter(meuble_g1)
inventaire_gauche_bas.ajouter(meuble_g2)
inventaire_gauche_bas.ajouter(meuble_g3)

inventaire_gauche_bas.ajouter(
    make_kick_drawer(name="Kick-toe g1", profondeur_kick_toe=g.PROFONDEUR_KICK_TOE_EVIER)
)
inventaire_gauche_bas.ajouter(
    make_kick_drawer(name="Kick-toe g2", profondeur_kick_toe=g.PROFONDEUR_KICK_TOE_GAUCHE)
)
inventaire_gauche_bas.ajouter(
    make_kick_drawer(name="Kick-toe g3", profondeur_kick_toe=g.PROFONDEUR_KICK_TOE_GAUCHE)
)
