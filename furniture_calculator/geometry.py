"""Constantes de dimensionnement de la cuisine (toutes en cm)."""

# =====================================================================
# Épaisseurs des planches
# =====================================================================

EPAISSEUR_PLANCHE = 19           # épaisseur planche standard
EPAISSEUR_PLAN_DE_TRAVAIL = 38    # épaisseur du plan de travail
EPAISSEUR_FOND_DE_MEUBLE = 3     # épaisseur du fond de meuble

# =====================================================================
# Côté gauche
# =====================================================================

PROFONDEUR_DISPONIBLE_GAUCHE = 670     # profondeur disponible gauche

MARGE_ARRIERE_GAUCHE_HAUT = 0.   # marge arrière gauche haut
MARGE_ARRIERE_GAUCHE_BAS = 50    # marge arrière gauche bas
PROFONDEUR_VIDE_SANITAIRE_EVIER = 150  # profondeur vide sanitaire évier

PROFONDEUR_MEUBLE_GAUCHE_BAS = PROFONDEUR_DISPONIBLE_GAUCHE - MARGE_ARRIERE_GAUCHE_BAS     # profondeur gauche bas
PROFONDEUR_MEUBLE_EVIER = PROFONDEUR_DISPONIBLE_GAUCHE - PROFONDEUR_VIDE_SANITAIRE_EVIER     # profondeur gauche bas

PROFONDEUR_MEUBLE_GAUCHE_HAUT = 379     # profondeur gauche haut

HAUTEUR_SOUS_PLAN_GAUCHE = 900   # hauteur sous plan de travail gauche
HAUTEUR_HAUT_GAUCHE = 900        # hauteur haut gauche
HAUTEUR_SOL_MEUBLE_HAUT = 1488   # hauteur sol -> meuble haut
HAUTEUR_FOND_EVIER = 300   # hauteur planche fond évier (laissep asser la tuyauterie)

# =====================================================================
# Côté droite
# =====================================================================

PROFONDEUR_DISPONIBLE_DROITE = 590      # profondeur disponible droite
MARGE_AVANT_DROITE = 5                 # marge avant droite
MARGE_ARRIERE_DROITE = 15         # marge arrière droite

PROFONDEUR_MEUBLE_DROITE = PROFONDEUR_DISPONIBLE_DROITE - MARGE_AVANT_DROITE - MARGE_ARRIERE_DROITE           # profondeur droite

HAUTEUR_BAS_DROITE = 950          # hauteur bas droite
HAUTEUR_DROITE = 2388             # hauteur droite (totale)
HAUTEUR_SUR_FRIGO = 1500          # hauteur sur frigo

# =====================================================================
# Kick-toe (plinthe)
# =====================================================================

PROFONDEUR_KICK_TOE = 550         # profondeur kick-toe
HAUTEUR_KICK_TOE = 149            # hauteur kick-toe
LARGEUR_KICK_TOE = 500            # largeur kick-toe
HAUTEUR_PORTE_KICK_TOE = 180      # hauteur porte kick-toe

# =====================================================================
# Fonds de meuble
# =====================================================================

PROFONDEUR_RAINURE_FOND = 3      # profondeur rainure du fond
PROFONDEUR_FOND_DE_MEUBLE = 10 + PROFONDEUR_RAINURE_FOND     # profondeur fond de meuble (encastré)
LARGEUR_RAINURE_FOND = 3         # largeur rainure du fond

# =====================================================================
# Tiroirs et portes
# =====================================================================

HAUTEUR_TIROIR_MIN = 120          # hauteur tiroir minimum

# =====================================================================
# Marges et tolérances
# =====================================================================

INCERTITUDE_SOL = 5              # incertitude de niveau du sol
MARGE_DEVANT_ETAGERE = 20         # marge devant étagère
MARGE_ENTRE_PLANCHE_FACADE = 3   # marge entre planche de façade

# =====================================================================
# Standards
# =====================================================================

LARGEUR_STANDARD = 600            # largeur standard de meuble
MILIEU_DE_COURSE_PIED = 12        # milieu de course du pied réglable

HAUTEUR_DEBUT_MEUBLE_BAS = INCERTITUDE_SOL + HAUTEUR_PORTE_KICK_TOE + MARGE_ENTRE_PLANCHE_FACADE
