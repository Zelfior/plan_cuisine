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
            f"prix_unitaire={self.prix_unitaire():.2f}€)"
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
                 compte: int = 0, parent: Optional["Meuble"] = None,
                 nom: Optional[str] = None):
        # arrondi à 2 décimales pour éviter le bruit des flottants
        # (69.89999999999999 -> 69.9) et stabiliser le hash
        self.longueur = round(
            self.longueur_defaut if longueur is None else longueur, 2
        )
        self.largeur = round(
            self.largeur_defaut if largeur is None else largeur, 2
        )
        self.couleur = self.couleur_defaut if couleur is None else couleur
        if self.couleur is None:
            raise ValueError("Aucune couleur définie pour cette planche.")
        if self.longueur <= 0 or self.largeur <= 0:
            raise ValueError(
                f"Dimensions invalides pour {self.__class__.__name__} : "
                f"{self.longueur}x{self.largeur} cm (négatives ou nulles)."
            )
        # nom de la planche : personnalisé, ou déduit des dimensions
        self.nom = nom or f"{self.longueur}x{self.largeur}"
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
                               self.compte, self.parent, self.nom)
        copie.historique = dict(self.historique)
        return copie

    __copy__ = copy

    @property
    def nom_complet(self) -> str:
        """Nom traçable : classe + nom (dimensions ou nom personnalisé)."""
        return f"{self.__class__.__name__} {self.nom}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.longueur}x{self.largeur}, "
            f"{self.couleur.name if self.couleur else '?'}, "
            f"compte={self.compte}, prix_unitaire={self.prix_unitaire:.2f}€, "
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
        self.inventaire: Optional["Inventaire"] = None  # rempli à l'ajout

    def ajouter(self, element: Union[Planche, Objet]) -> None:
        if isinstance(element, Planche):
            cible = self.planches
        elif isinstance(element, Objet):
            cible = self.objets
        else:
            raise TypeError(f"Type non supporté : {type(element)!r}")
        element.parent = self
        # nom unique pour une planche : si le nom est déjà pris dans ce
        # meuble, on suffixe (_2, _3, ...) pour tracer chaque instance
        if isinstance(element, Planche):
            noms_pris = {p.nom for p in self.planches}
            if element.nom in noms_pris:
                base = element.nom
                k = 2
                while f"{base}_{k}" in noms_pris:
                    k += 1
                element.nom = f"{base}_{k}"
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
        # refuse un doublon si ce meuble appartient à un inventaire
        if (self.inventaire is not None
                and any(m.nom == nouveau_nom
                        for m in self.inventaire.meubles if m is not self)):
            raise ValueError(
                f"Un meuble nommé {nouveau_nom!r} existe déjà dans "
                f"l'inventaire."
            )
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
        if any(m.nom == meuble.nom for m in self.meubles):
            raise ValueError(
                f"Un meuble nommé {meuble.nom!r} existe déjà dans l'inventaire."
            )
        meuble.inventaire = self
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
                prix_u_txt = f"{prix_u:.2f}€/u"
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
                f"{planche.longueur}x{planche.largeur} "
                f"({planche.couleur.name}, {planche.prix_m2:.2f}€/m²): "
                f"{total_par_planche[cle]} u x "
                f"{planche.prix_unitaire:.2f}€/u = {total:.2f}€"
            )
            for parent, qte in historique_par_planche[cle].items():
                lignes.append(f"    {parent} -> {qte}")

        lignes.append("--- Total ---")
        lignes.append(f"Prix total de l'inventaire : {self.prix_total:.2f}€")
        return "\n".join(lignes)

    @property
    def prix_total(self) -> float:
        return sum(m.prix_total for m in self.meubles)

    # ------------------------------------------------------------- bilan MD
    def _collecte(self):
        """Regroupe planches (par hash) et objets (par classe) par meuble.

        Renvoie (noms_meubles, planches, objets, detail_planches) où :
        - planches : {hash: {"ex": Planche, "par_meuble": {nom: qte}}}
        - objets   : {classe: {"par_meuble": {nom: qte}}}
        - detail_planches : {hash: {nom_meuble: [(nom_planche, qte)]}}
          pour tracer, dans la répartition, où va chaque type + taille.
        """
        noms = [m.nom for m in self.meubles]
        planches: Dict[int, Dict] = {}
        objets: Dict[type, Dict] = {}
        detail: Dict[int, Dict[str, list]] = {}
        for meuble in self.meubles:
            for planche in meuble.planches:
                cle = hash(planche)
                entree = planches.setdefault(
                    cle, {"ex": planche, "par_meuble": {}}
                )
                entree["par_meuble"][meuble.nom] = (
                    entree["par_meuble"].get(meuble.nom, 0) + planche.compte
                )
                par_meuble = detail.setdefault(cle, {})
                tailles = par_meuble.setdefault(meuble.nom, [])
                # agrège par nom de planche dans ce meuble
                deja_present = False
                nouvelles_tailles = []
                for n, q in tailles:
                    if n == planche.nom:
                        deja_present = True
                        q += planche.compte
                    nouvelles_tailles.append((n, q))
                if not deja_present:
                    nouvelles_tailles.append((planche.nom, planche.compte))
                par_meuble[meuble.nom] = nouvelles_tailles
            for objet in meuble.objets:
                cls = objet.__class__
                entree = objets.setdefault(cls, {"par_meuble": {}})
                entree["par_meuble"][meuble.nom] = (
                    entree["par_meuble"].get(meuble.nom, 0) + objet.compte
                )
        return noms, planches, objets, detail

    def bilan_markdown(self) -> str:
        """Rédige un bilan Markdown de l'inventaire.

        1. un tableau des planches (type, dimensions, couleur, nombre, prix) ;
        2. un tableau des objets (type, nombre, prix) ;
        3. un tableau géant croisant chaque planche / objet avec chaque meuble.
        """
        noms, planches, objets, detail = self._collecte()
        lignes: List[str] = ["# Bilan de l'inventaire", ""]

        # -------------------------------------------------- tableau planches
        lignes += [
            "## Planches",
            "",
            "| Type | Longueur (cm) | Largeur (cm) | Couleur | Nombre | Prix/u (€) | Total (€) |",
            "|---|---:|---:|---|---:|---:|---:|",
        ]
        for entree in planches.values():
            p = entree["ex"]
            nombre = sum(entree["par_meuble"].values())
            lignes.append(
                f"| {p.nom_complet} | {p.longueur} | {p.largeur} "
                f"| {p.couleur.name} | {nombre} "
                f"| {p.prix_unitaire:.2f} "
                f"| {nombre * p.prix_unitaire:.2f} |"
            )
        lignes.append("")

        # --------------------------------------------------- tableau objets
        lignes += [
            "## Objets",
            "",
            "| Type | Nombre | Prix/u (€) | Total (€) |",
            "|---|---:|---:|---:|",
        ]
        for cls, entree in objets.items():
            nombre = sum(entree["par_meuble"].values())
            try:
                prix_u = cls.prix_unitaire()
                lignes.append(
                    f"| {cls.__name__} | {nombre} | {prix_u:.2f} "
                    f"| {nombre * prix_u:.2f} |"
                )
            except (ValueError, ZeroDivisionError):
                lignes.append(f"| {cls.__name__} | {nombre} | #DIV/0! | |")
        lignes.append("")

        # --------------------------------------------- tableau géant croisé
        lignes += [
            "## Répartition par meuble",
            "",
            "| Élément | " + " | ".join(noms) + " | Total |",
            "|---|" + "|".join(["---:"] * (len(noms) + 1)) + "|",
        ]
        # planches : une ligne par type + taille, cellules "nombre: noms"
        # pour tracer où va chaque planche
        for cle, par_meuble in detail.items():
            p = planches[cle]["ex"]
            libelle = (f"{p.__class__.__name__} {p.longueur}x{p.largeur} "
                       f"({p.couleur.name})")
            cases = []
            total = 0
            for nom in noms:
                tailles = par_meuble.get(nom, [])
                qte = sum(q for _, q in tailles)
                total += qte
                if not tailles:
                    cases.append("0")
                else:
                    noms_txt = "<br>".join(
                        n if q == 1 else f"{n} (x{q})" for n, q in tailles
                    )
                    cases.append(f"{qte}: {noms_txt}")
            lignes.append(
                f"| {libelle} | " + " | ".join(cases) + f" | {total} |"
            )
        for cls, entree in objets.items():
            cases = [str(entree["par_meuble"].get(nom, 0)) for nom in noms]
            total = sum(entree["par_meuble"].values())
            lignes.append(f"| {cls.__name__} | " + " | ".join(cases) + f" | {total} |")
        lignes.append("")

        lignes.append(f"**Prix total de l'inventaire : {self.prix_total:.2f} €**")
        return "\n".join(lignes)

    def ecrire_bilan_markdown(self, chemin: str = "bilan.md") -> str:
        """Écrit le bilan Markdown dans un fichier (utf-8)."""
        contenu = self.bilan_markdown()
        with open(chemin, "w", encoding="utf-8") as fichier:
            fichier.write(contenu + "\n")
        return chemin


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
    print()
    print(inv.bilan_markdown())