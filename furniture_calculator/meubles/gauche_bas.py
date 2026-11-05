import geometry as g
from model import *


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
    - g.PROFONDEUR_FOND_DE_MEUBLE
    - g.PROFONDEUR_VIDE_SANITAIRE
)

PROFONDEUR_CAISSON_EVIER = (
    g.PROFONDEUR_MEUBLE_GAUCHE_BAS
    - g.EPAISSEUR_PLANCHE
    - g.PROFONDEUR_FOND_DE_MEUBLE
    - g.PROFONDEUR_VIDE_SANITAIRE_EVIER
)

HAUTEUR_FOND = (
    g.HAUTEUR_SOUS_PLAN_GAUCHE
    - g.INCERTITUDE_SOL
    - g.HAUTEUR_PORTE_KICK_TOE
    - g.EPAISSEUR_PLANCHE
    + g.LARGEUR_RAINURE_FOND
)

LARGEUR_FOND = (
    LARGEUR_INTERIEURE + 2 * g.LARGEUR_RAINURE_FOND
)

LARGEUR_FACADE = (
    g.LARGEUR_STANDARD - g.MARGE_ENTRE_PLANCHE_FACADE
)


# ============================================================
# STRUCTURE COMMUNE
# ============================================================

def ajouter_structure_meuble(meuble, profondeur_caisson=PROFONDEUR_CAISSON, hauteur_caisson=HAUTEUR_CAISSON):

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
            largeur=LARGEUR_INTERIEURE,
            compte=1,
            nom="Base"
        )
    )

    meuble.ajouter(
        PlancheFond(
            longueur=HAUTEUR_FOND,
            largeur=LARGEUR_FOND,
            compte=1,
            nom="Fond"
        )
    )

    meuble.ajouter(Vis(compte=6))
    meuble.ajouter(Tourillon(compte=4))


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
          - PROFONDEUR_FOND_DE_MEUBLE
          - PROFONDEUR_VIDE_SANITAIRE

Fond -- profondeur PROFONDEUR_FOND_DE_MEUBLE

Vide sanitaire -- PROFONDEUR_VIDE_SANITAIRE
"""

ajouter_structure_meuble(meuble_g1, profondeur_caisson=PROFONDEUR_CAISSON_EVIER)

meuble_g1.ajouter(
    PlancheVert(
        longueur=(
            g.HAUTEUR_SOUS_PLAN_GAUCHE
            - g.HAUTEUR_DEBUT_MEUBLE_BAS
            - 2 * g.MARGE_ENTRE_PLANCHE_FACADE
        ),
        largeur=LARGEUR_FACADE,
        compte=1,
        nom="Porte"
    )
)

meuble_g1.ajouter(CharnierePorte(compte=2))


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
          - PROFONDEUR_FOND_DE_MEUBLE
          - PROFONDEUR_VIDE_SANITAIRE

Fond -- profondeur PROFONDEUR_FOND_DE_MEUBLE

Vide sanitaire -- PROFONDEUR_VIDE_SANITAIRE
"""

ajouter_structure_meuble(meuble_g2)

meuble_g2.ajouter(
    PlancheBlanc(
        longueur=(
            g.PROFONDEUR_MEUBLE_GAUCHE_BAS
            - g.MARGE_DEVANT_ETAGERE
            - g.EPAISSEUR_PLANCHE
            - g.PROFONDEUR_FOND_DE_MEUBLE
            - g.MARGE_ARRIERE_GAUCHE_BAS
        ),
        largeur=LARGEUR_INTERIEURE,
        compte=1,
        nom="Etagère"
    )
)

meuble_g2.ajouter(PionSupportEtagere(compte=4))


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

ajouter_structure_meuble(meuble_g3)

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
        largeur=LARGEUR_FACADE,
        compte=2,
        nom="Porte tiroir bas"
    )
)

meuble_g3.ajouter(
    PlancheVert(
        longueur=HAUTEUR_TIROIR_RESTANT,
        largeur=LARGEUR_FACADE,
        compte=1,
        nom="Porte tiroir reste"
    )
)

meuble_g3.ajouter(
    PlancheVert(
        longueur=HAUTEUR_TIROIR_MAX,
        largeur=LARGEUR_FACADE,
        compte=1,
        nom="Porte tiroir haut"
    )
)


# ============================================================
# KICK DRAWER
# ============================================================

# To be refined

kick_drawer = Meuble(nom="Kick Drawer")

kick_drawer.ajouter(
    PlancheVert(
        longueur=g.HAUTEUR_PORTE_KICK_TOE,
        largeur=LARGEUR_FACADE,
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
        longueur=g.PROFONDEUR_KICK_TOE,
        largeur=g.LARGEUR_KICK_TOE,
        compte=1,
        nom="Base kick-toe"
    )
)


# ============================================================
# INVENTAIRE
# ============================================================

inventaire = Inventaire()

inventaire.ajouter(meuble_g1)
inventaire.ajouter(meuble_g2)
inventaire.ajouter(meuble_g3)
inventaire.ajouter(kick_drawer)

inventaire.ecrire_bilan_markdown("bilan.md")

print(inventaire.bilan())
