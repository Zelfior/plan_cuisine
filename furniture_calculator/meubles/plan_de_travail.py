
import furniture_calculator.geometry as g
from furniture_calculator.model import *
from furniture_calculator.meubles.gauche_bas import ajouter_base_meuble

plan_gauche = PlanchePlan(
    longueur = g.LONGUEUR_PLAN_DE_TRAVAIL,
    largeur = g.PROFONDEUR_PLAN_DE_TRAVAIL,
    compte = 1,
    nom = "Gauche"
)

meuble_plans = Meuble("Plans")
meuble_plans.ajouter(plan_gauche)

inventaire_plan_de_travail = Inventaire()
inventaire_plan_de_travail.ajouter(meuble_plans)
