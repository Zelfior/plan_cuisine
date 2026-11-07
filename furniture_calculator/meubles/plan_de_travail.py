
import furniture_calculator.geometry as g
from furniture_calculator.model import *
from furniture_calculator.meubles.gauche_bas import ajouter_base_meuble

plan_gauche = PlanchePlan(
    longueur = g.LONGUEUR_PLAN_DE_TRAVAIL,
    largeur = g.PROFONDEUR_PLAN_DE_TRAVAIL,
    compte = 1,
    nom = "Gauche"
)
plan_droite = PlanchePlanFin(
    longueur = 2 * (g.LARGEUR_STANDARD - g.EPAISSEUR_PLANCHE * 2 - g.MARGE_PORTE_COULISSANTE),
    largeur = g.PROFONDEUR_MEUBLE_DROITE - g.EPAISSEUR_PLANCHE - g.PROFONDEUR_FOND_DE_MEUBLE,
    compte = 1,
    nom = "droite"
)

meuble_plans = Meuble("Plans")
meuble_plans.ajouter(plan_gauche)
meuble_plans.ajouter(plan_droite)

inventaire_plan_de_travail = Inventaire()
inventaire_plan_de_travail.ajouter(meuble_plans)
