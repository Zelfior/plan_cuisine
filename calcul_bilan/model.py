"""Inventaire de meubles : planches, quincaillerie et bilan de stock."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional, Union


class Couleur(Enum):
    """Finition d'une planche."""
    BLANC = auto()
    VERT = auto()
    FOND = auto()


@dataclass(frozen=True)
class Lot:
    """Lot d'achat : prix du lot, nombre d'unités, url fournisseur."""
    prix_lot: float
    unites: int
    url: str = ""

    @property
    def prix_unitaire(self) -> float:
        if self.unites == 0:
            raise ZeroDivisionError(
                f"Lot sans unité : prix unitaire indéterminé (#DIV/0!)."
            )
        return self.prix_lot / self.unites


class Objet:
    """Quincaillerie comptable.

    Hashable (sur le nom de classe), possède un meuble parent et un compte
    d'unités. L'addition et la multiplication modifient ce compte en
    conservant l'historique des parents. Le prix unitaire est calculé
    à partir d'un lot et d'une url.
    """

    lot: Optional[Lot] = None  # à définir par chaque classe enfant

    def __init__(self, compte: int = 0, parent: Optional["Meuble"] = None):
        self.compte = compte
        self.parent = parent
        # historique des apports : nom du parent -> quantité reçue
        self.historique: Dict[str, int] = {}
        if parent is not None and compte:
            self.historique[parent.nom] = (
                self.historique.get(parent.nom, 0) + compte
            )

    # ---------------------------------------------------------------- hash
    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Objet) and hash(self) == hash(other)

    # --------------------------------------------------------------- prix
    @classmethod
    def prix_unitaire(cls) -> float:
        """Prix par unité, calculé à partir du lot (et de son url)."""
        if cls.lot is None:
            raise ValueError(f"Aucun lot défini pour {cls.__name__}.")
        return cls.lot.prix_unitaire

    @property
    def prix_total(self) -> float:
        return self.compte * self.prix_unitaire()

    # ---------------------------------------------------------- opérateurs
    def __add__(self, other: "Objet") -> "Objet":
        """Additionne deux objets de même type : les comptes s'ajoutent."""
        if not isinstance(other, Objet) or hash(self) != hash(other):
            return NotImplemented
        resultat = self.__class__(self.compte + other.compte)
        resultat.historique = dict(self.historique)
        for nom, qte in other.historique.items():
            resultat.historique[nom] = resultat.historique.get(nom, 0) + qte
        return resultat

    def __mul__(self, facteur: int) -> "Objet":
        """Multiplie le compte par un facteur."""
        if isinstance(facteur, bool) or not isinstance(facteur, int):
            return NotImplemented
        resultat = self.__class__(self.compte * facteur)
        resultat.historique = {
            nom: qte * facteur for nom, qte in self.historique.items()
        }
        return resultat

    __rmul__ = __mul__

    # --------------------------------------------------------------- copie
    def copy(self) -> "Objet":
        """Copie indépendante : même classe, même compte et historique."""
        copie = self.__class__(self.compte, self.parent)
        copie.historique = dict(self.historique)
        return copie

    __copy__ = copy

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(compte={self.compte}, "
            f"prix_unitaire={self.prix_unitaire():.4f}€)"
        )


class Planche:
    """Planche avec compte et parent, plus longueur, largeur et couleur.

    Le hash prend en compte longueur, largeur, couleur et prix au m².
    """

    prix_m2: float = 0.0          # prix au m², à définir par la classe enfant
    epaisseur_cm: float = 0.0     # épaisseur de la plaque
    masse_par_cm2: float = 0.0    # masse d'une plaque (kg par cm²)
    longueur_defaut: float = 0.0  # dimensions de la plaque entière
    largeur_defaut: float = 0.0
    couleur_defaut: Optional[Couleur] = None

    def __init__(self, longueur: Optional[float] = None,
                 largeur: Optional[float] = None,
                 couleur: Optional[Couleur] = None,
                 compte: int = 0, parent: Optional["Meuble"] = None):
        self.longueur = self.longueur_defaut if longueur is None else longueur
        self.largeur = self.largeur_defaut if largeur is None else largeur
        self.couleur = self.couleur_defaut if couleur is None else couleur
        if self.couleur is None:
            raise ValueError("Aucune couleur définie pour cette planche.")
        self.compte = compte
        self.parent = parent
        self.historique: Dict[str, int] = {}
        if parent is not None and compte:
            self.historique[parent.nom] = (
                self.historique.get(parent.nom, 0) + compte
            )

    # ---------------------------------------------------------------- hash
    def __hash__(self) -> int:
        return hash((self.longueur, self.largeur, self.couleur, self.prix_m2))

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Planche) and hash(self) == hash(other)

    # --------------------------------------------------------------- prix
    @property
    def surface_m2(self) -> float:
        return (self.longueur * self.largeur) / 10_000.0  # cm -> m²

    @property
    def prix_unitaire(self) -> float:
        return self.surface_m2 * self.prix_m2

    @property
    def masse(self) -> float:
        """Masse totale (kg) pour le compte courant."""
        return self.compte * self.longueur * self.largeur * self.masse_par_cm2

    @property
    def prix_total(self) -> float:
        return self.compte * self.prix_unitaire

    # ---------------------------------------------------------- opérateurs
    def __add__(self, other: "Planche") -> "Planche":
        if not isinstance(other, Planche) or hash(self) != hash(other):
            return NotImplemented
        resultat = self.__class__(self.longueur, self.largeur, self.couleur,
                                  self.compte + other.compte)
        resultat.historique = dict(self.historique)
        for nom, qte in other.historique.items():
            resultat.historique[nom] = resultat.historique.get(nom, 0) + qte
        return resultat

    def __mul__(self, facteur: int) -> "Planche":
        if isinstance(facteur, bool) or not isinstance(facteur, int):
            return NotImplemented
        resultat = self.__class__(self.longueur, self.largeur, self.couleur,
                                  self.compte * facteur)
        resultat.historique = {
            nom: qte * facteur for nom, qte in self.historique.items()
        }
        return resultat

    __rmul__ = __mul__

    # --------------------------------------------------------------- copie
    def copy(self) -> "Planche":
        """Copie indépendante : mêmes dimensions, couleur, compte, historique."""
        copie = self.__class__(self.longueur, self.largeur, self.couleur,
                               self.compte, self.parent)
        copie.historique = dict(self.historique)
        return copie

    __copy__ = copy

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.longueur}x{self.largeur}, "
            f"{self.couleur.name if self.couleur else '?'}, "
            f"compte={self.compte}, prix_unitaire={self.prix_unitaire:.4f}€, "
            f"masse={self.masse:.2f}kg)"
        )


# =====================================================================
# Classes enfants de Planche : types de plaques
# (épaisseur cm, masse kg/cm², dimensions plaque entière cm, prix €/m²)
# =====================================================================

class PlanchePlan(Planche):
    epaisseur_cm = 3.8
    masse_par_cm2 = 0.002439024
    longueur_defaut = 410
    largeur_defaut = 65
    prix_m2 = 71.08
    couleur_defaut = Couleur.BLANC  # plan brut, finition non définie


class PlancheBlanc(Planche):
    epaisseur_cm = 1.9
    masse_par_cm2 = 0.001380262
    longueur_defaut = 280
    largeur_defaut = 207
    prix_m2 = 20.04
    couleur_defaut = Couleur.BLANC


class PlancheVert(Planche):
    epaisseur_cm = 1.9
    masse_par_cm2 = 0.001444099
    longueur_defaut = 280
    largeur_defaut = 207
    prix_m2 = 56.35
    couleur_defaut = Couleur.VERT


class PlancheFond(Planche):
    epaisseur_cm = 0.3
    masse_par_cm2 = 0.000319444
    longueur_defaut = 120
    largeur_defaut = 60
    prix_m2 = 3.49
    couleur_defaut = Couleur.FOND


# =====================================================================
# Classes enfants d'Objet : quincaillerie
# (prix unitaire, prix lot, unités par lot)
# =====================================================================

class CharnierePorte(Objet):
    lot = Lot(15.90, 4)


class SupportMeubleReglable(Objet):
    lot = Lot(25.84, 8)


class AttacheMontantDeco(Objet):
    lot = Lot(15.80, 20)


class GlissierePorte(Objet):
    lot = Lot(69.00, 2)


class RailKickToe(Objet):
    lot = Lot(11.30, 2)


class Vis(Objet):
    lot = Lot(31.49, 50)


class ChevilleMurale(Objet):
    lot = Lot(18.90, 50)


class Rail2m(Objet):
    lot = None  # #DIV/0! : prix de lot inconnu -> prix unitaire indéterminé


class CrochetMural(Objet):
    lot = Lot(11.90, 4)


class Tourillon(Objet):
    lot = Lot(3.00, 40)


class TiroirHaut(Objet):
    lot = Lot(56.00, 1)


class TiroirMoyen(Objet):
    lot = Lot(41.00, 1)


class TiroirBas(Objet):
    lot = Lot(34.00, 1)


class MultiPrise(Objet):
    lot = Lot(34.90, 1)


class PionSupportEtagere(Objet):
    lot = Lot(15.33, 20)


# =====================================================================
# Meuble et Inventaire
# =====================================================================

class Meuble:
    """Un meuble : une liste de planches et une liste d'objets."""

    def __init__(self, nom: str):
        self.nom = nom
        self.planches: List[Planche] = []
        self.objets: List[Objet] = []

    def ajouter(self, element: Union[Planche, Objet]) -> None:
        if isinstance(element, Planche):
            cible = self.planches
        elif isinstance(element, Objet):
            cible = self.objets
        else:
            raise TypeError(f"Type non supporté : {type(element)!r}")
        element.parent = self
        element.historique[self.nom] = (
            element.historique.get(self.nom, 0) + element.compte
        )
        cible.append(element)

    @property
    def prix_total(self) -> float:
        return (sum(p.prix_total for p in self.planches)
                + sum(o.prix_total for o in self.objets))

    # --------------------------------------------------------------- copie
    def copy(self) -> "Meuble":
        """Copie indépendante du meuble, avec copies de ses éléments.

        Les copies gardent l'original comme parent (référence conservée)
        mais leur historique est dupliqué, donc modifiable sans effet.
        """
        copie = Meuble(self.nom)
        for planche in self.planches:
            copie.planches.append(planche.copy())
        for objet in self.objets:
            copie.objets.append(objet.copy())
        return copie

    __copy__ = copy

    # ------------------------------------------------------------- renommage
    def rename(self, nouveau_nom: str) -> None:
        """Renomme le meuble et met à jour le parent chez tous ses enfants.

        La clé correspondant à l'ancien nom est renommée dans l'historique
        de chaque planche et objet, en conservant les quantités.
        """
        ancien_nom = self.nom
        if nouveau_nom == ancien_nom:
            return
        for enfant in self.planches + self.objets:
            enfant.parent = self
            if ancien_nom in enfant.historique:
                enfant.historique[nouveau_nom] = enfant.historique.pop(
                    ancien_nom
                )
        self.nom = nouveau_nom

    def __repr__(self) -> str:
        return f"Meuble({self.nom!r}, {len(self.planches)} planches, {len(self.objets)} objets)"


class Inventaire:
    """Une liste de meubles, avec bilan global de tout ce qui est contenu."""

    def __init__(self):
        self.meubles: List[Meuble] = []

    def ajouter(self, meuble: Meuble) -> None:
        self.meubles.append(meuble)

    # --------------------------------------------------------------- copie
    def copy(self) -> "Inventaire":
        """Copie indépendante de l'inventaire (meubles et contenu copiés)."""
        copie = Inventaire()
        copie.meubles = [meuble.copy() for meuble in self.meubles]
        return copie

    __copy__ = copy

    def bilan(self) -> str:
        """Récapitule, par type, qui a besoin de combien, plus le total."""
        lignes: List[str] = []

        # Objets : agrège les comptes et historiques par classe
        total_par_type: Dict[type, int] = {}
        historique_par_type: Dict[type, Dict[str, int]] = {}
        for meuble in self.meubles:
            for objet in meuble.objets:
                cls = objet.__class__
                total_par_type[cls] = total_par_type.get(cls, 0) + objet.compte
                hist = historique_par_type.setdefault(cls, {})
                for parent, qte in objet.historique.items():
                    hist[parent] = hist.get(parent, 0) + qte
        lignes.append("--- Objets ---")
        for cls in total_par_type:
            try:
                prix_u = cls.prix_unitaire()
                prix_u_txt = f"{prix_u:.4f}€/u"
                total = total_par_type[cls] * prix_u
            except (ValueError, ZeroDivisionError):
                prix_u_txt = "#DIV/0!"
                total = float("nan")
            lignes.append(f"{cls.__name__}: {total_par_type[cls]} u "
                          f"x {prix_u_txt} = {total:.2f}€")
            for parent, qte in historique_par_type[cls].items():
                lignes.append(f"    {parent} -> {qte}")

        # Planches : agrège les comptes et historiques par hash
        total_par_planche: Dict[int, int] = {}
        exemplaires: Dict[int, Planche] = {}
        historique_par_planche: Dict[int, Dict[str, int]] = {}
        for meuble in self.meubles:
            for planche in meuble.planches:
                cle = hash(planche)
                exemplaires.setdefault(cle, planche)
                total_par_planche[cle] = (
                    total_par_planche.get(cle, 0) + planche.compte
                )
                hist = historique_par_planche.setdefault(cle, {})
                for parent, qte in planche.historique.items():
                    hist[parent] = hist.get(parent, 0) + qte
        lignes.append("--- Planches ---")
        for cle, planche in exemplaires.items():
            total = planche.prix_unitaire * total_par_planche[cle]
            lignes.append(
                f"{planche.longueur:.2f}x{planche.largeur:.2f} "
                f"({planche.couleur.name}, {planche.prix_m2:.2f}€/m²): "
                f"{total_par_planche[cle]} u x "
                f"{planche.prix_unitaire:.4f}€/u = {total:.2f}€"
            )
            for parent, qte in historique_par_planche[cle].items():
                lignes.append(f"    {parent} -> {qte}")

        lignes.append("--- Total ---")
        lignes.append(f"Prix total de l'inventaire : {self.prix_total:.2f}€")
        return "\n".join(lignes)

    @property
    def prix_total(self) -> float:
        return sum(m.prix_total for m in self.meubles)


if __name__ == "__main__":
    # Exemple d'utilisation
    inv = Inventaire()
    caisse = Meuble("Caisse cuisine")
    caisse.ajouter(PlancheBlanc(280, 207, compte=2))
    caisse.ajouter(PlancheFond(120, 60, compte=1))
    caisse.ajouter(CharnierePorte(4))
    inv.ajouter(caisse)

    etagere = Meuble("Étagère salon")
    etagere.ajouter(PlancheVert(compte=3))          # plaque entière 280x207
    etagere.ajouter(PlanchePlan(410, 65, compte=2))  # plan 3,8 cm
    etagere.ajouter(Vis(8))
    inv.ajouter(etagere)

    print(inv.bilan())