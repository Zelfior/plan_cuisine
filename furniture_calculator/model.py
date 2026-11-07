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

class ChampDirection(Enum):
    """Direction du champ."""
    L1 = auto()
    L2 = auto()
    G1 = auto()
    G2 = auto()

L1 = ChampDirection.L1
L2 = ChampDirection.L2
G1 = ChampDirection.G1
G2 = ChampDirection.G2

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

    def __init__(
        self,
        longueur: Optional[float] = None,
        largeur: Optional[float] = None,
        couleur: Optional[Couleur] = None,
        compte: int = 0, parent: Optional["Meuble"] = None,
        nom: Optional[str] = None,
        champ: List[ChampDirection] = None
    ):
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
        self.champ = champ if champ is not None else []
        if parent is not None and compte:
            self.historique[parent.nom] = (
                self.historique.get(parent.nom, 0) + compte
            )

    # ---------------------------------------------------------------- hash
    def __hash__(self) -> int:
        return hash((
            self.longueur,
            self.largeur,
            self.couleur,
            self.prix_m2,
            tuple(self.champ)
        ))

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Planche)
            and self.longueur == other.longueur
            and self.largeur == other.largeur
            and self.couleur == other.couleur
            and self.prix_m2 == other.prix_m2
            and self.champ == other.champ
        )

    # --------------------------------------------------------------- prix
    @property
    def surface_m2(self) -> float:
        return (self.longueur * self.largeur) / 1000_000.0  # cm -> m²

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

        resultat = self.__class__(
            self.longueur,
            self.largeur,
            self.couleur,
            self.compte + other.compte,
            champ=self.champ
        )
        resultat.historique = dict(self.historique)
        for nom, qte in other.historique.items():
            resultat.historique[nom] = resultat.historique.get(nom, 0) + qte

        return resultat


    def __mul__(self, facteur: int) -> "Planche":
        if isinstance(facteur, bool) or not isinstance(facteur, int):
            return NotImplemented

        resultat = self.__class__(
            self.longueur,
            self.largeur,
            self.couleur,
            self.compte * facteur,
            champ=self.champ
        )
        resultat.historique = {
            nom: qte * facteur for nom, qte in self.historique.items()
        }
        return resultat


    def copy(self) -> "Planche":
        copie = self.__class__(
            self.longueur,
            self.largeur,
            self.couleur,
            self.compte,
            self.parent,
            self.nom,
            champ=self.champ.copy()
        )
        copie.historique = dict(self.historique)
        return copie

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
    lot = Lot(10, 1)


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

    # --------------------------------------------------------------- bilan
    def bilan(self) -> str:
        """Récapitule les planches, objets et le prix total."""

        lignes: List[str] = []

        # Objets : agrégation par classe
        total_par_type: Dict[type, int] = {}
        historique_par_type: Dict[type, Dict[str, int]] = {}

        for meuble in self.meubles:
            for objet in meuble.objets:
                cls = objet.__class__
                total_par_type[cls] = (
                    total_par_type.get(cls, 0) + objet.compte
                )
                hist = historique_par_type.setdefault(cls, {})
                for parent, qte in objet.historique.items():
                    hist[parent] = hist.get(parent, 0) + qte

        lignes.append("--- Objets ---")

        for cls, quantite in total_par_type.items():
            try:
                prix_u = cls.prix_unitaire()
                prix_u_txt = f"{prix_u:.2f}€/u"
                total = quantite * prix_u
            except (ValueError, ZeroDivisionError):
                prix_u_txt = "#DIV/0!"
                total = float("nan")

            lignes.append(
                f"{cls.__name__}: {quantite} u "
                f"x {prix_u_txt} = {total:.2f}€"
            )

            for parent, qte in historique_par_type[cls].items():
                lignes.append(f"    {parent} -> {qte}")

        # Planches : agrégation par hash (dimensions, couleur, prix, champ)
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
            quantite = total_par_planche[cle]
            total = planche.prix_unitaire * quantite
            champ_txt = ", ".join(c.name for c in planche.champ) or "-"

            lignes.append(
                f"{planche.nom_complet} "
                f"({planche.longueur}x{planche.largeur}, "
                f"{planche.couleur.name}, "
                f"{planche.prix_m2:.2f}€/m², "
                f"Champ: {champ_txt}): "
                f"{quantite} u x "
                f"{planche.prix_unitaire:.2f}€/u = {total:.2f}€"
            )

            for parent, qte in historique_par_planche[cle].items():
                lignes.append(f"    {parent} -> {qte}")

        lignes.append("--- Total ---")
        lignes.append(
            f"Prix total de l'inventaire : {self.prix_total:.2f}€"
        )

        return "\n".join(lignes)

    @property
    def prix_total(self) -> float:
        return sum(m.prix_total for m in self.meubles)

    # ------------------------------------------------------------- collecte
    def _collecte(self):
        """Regroupe planches (par hash) et objets (par classe) par meuble.

        Renvoie :
        - noms_meubles
        - planches
        - objets
        - detail_planches
        """

        noms = [m.nom for m in self.meubles]

        planches: Dict[int, Dict] = {}
        objets: Dict[type, Dict] = {}
        detail: Dict[int, Dict[str, list]] = {}

        for meuble in self.meubles:

            for planche in meuble.planches:
                cle = hash(planche)

                entree = planches.setdefault(
                    cle, {
                        "ex": planche,
                        "par_meuble": {}
                    }
                )

                entree["par_meuble"][meuble.nom] = (
                    entree["par_meuble"].get(meuble.nom, 0)
                    + planche.compte
                )

                par_meuble = detail.setdefault(cle, {})
                tailles = par_meuble.setdefault(meuble.nom, [])

                # Agrégation par nom de planche
                deja_present = False
                nouvelles_tailles = []

                for n, q in tailles:
                    if n == planche.nom:
                        deja_present = True
                        q += planche.compte

                    nouvelles_tailles.append((n, q))

                if not deja_present:
                    nouvelles_tailles.append(
                        (planche.nom, planche.compte)
                    )

                par_meuble[meuble.nom] = nouvelles_tailles

            for objet in meuble.objets:
                cls = objet.__class__

                entree = objets.setdefault(
                    cls, {"par_meuble": {}}
                )

                entree["par_meuble"][meuble.nom] = (
                    entree["par_meuble"].get(meuble.nom, 0)
                    + objet.compte
                )

        return noms, planches, objets, detail

    # ------------------------------------------------------ bilan Markdown
    def bilan_markdown(self) -> str:
        """Rédige un bilan Markdown de l'inventaire."""

        noms, planches, objets, detail = self._collecte()

        lignes: List[str] = [
            "# Bilan de l'inventaire",
            ""
        ]

        # -------------------------------------------------- tableau planches
        lignes += [
            "## Planches",
            "",
            "| Type | Longueur (cm) | Largeur (cm) | Couleur | Champ | Nombre | Prix/u (€) | Total (€) |",
            "|---|---:|---:|---|---|---:|---:|---:|",
        ]

        for entree in planches.values():
            p = entree["ex"]
            nombre = sum(entree["par_meuble"].values())
            champ_txt = ", ".join(c.name for c in p.champ) or "-"

            lignes.append(
                f"| {p.nom_complet} "
                f"| {p.longueur} "
                f"| {p.largeur} "
                f"| {p.couleur.name} "
                f"| {champ_txt} "
                f"| {nombre} "
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
                    f"| {cls.__name__} "
                    f"| {nombre} "
                    f"| {prix_u:.2f} "
                    f"| {nombre * prix_u:.2f} |"
                )

            except (ValueError, ZeroDivisionError):
                lignes.append(
                    f"| {cls.__name__} | {nombre} | #DIV/0! | |"
                )

        lignes.append("")

        # --------------------------------------------- tableau de répartition
        lignes += [
            "## Répartition par meuble",
            "",
            "| Élément | " + " | ".join(noms) + " | Total |",
            "|---|" + "|".join(["---:"] * (len(noms) + 1)) + "|",
        ]

        # Planches : une ligne par type, dimensions, couleur et champ
        for cle, par_meuble in detail.items():
            p = planches[cle]["ex"]

            champ_txt = ", ".join(c.name for c in p.champ) or "-"

            libelle = (
                f"{p.__class__.__name__} "
                f"{p.longueur}x{p.largeur} "
                f"({p.couleur.name}, Champ: {champ_txt})"
            )

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
                        n if q == 1 else f"{n} (x{q})"
                        for n, q in tailles
                    )
                    cases.append(f"{qte}: {noms_txt}")

            lignes.append(
                f"| {libelle} | "
                + " | ".join(cases)
                + f" | {total} |"
            )

        # Objets
        for cls, entree in objets.items():
            cases = [
                str(entree["par_meuble"].get(nom, 0))
                for nom in noms
            ]

            total = sum(entree["par_meuble"].values())

            lignes.append(
                f"| {cls.__name__} | "
                + " | ".join(cases)
                + f" | {total} |"
            )

        lignes.append("")

        lignes.append(
            f"**Prix total de l'inventaire : "
            f"{self.prix_total:.2f} €**"
        )

        return "\n".join(lignes)

    # --------------------------------------------------------- fichier MD
    def ecrire_bilan_markdown(
        self, chemin: str = "bilan.md"
    ) -> str:
        """Écrit le bilan Markdown dans un fichier (utf-8)."""

        contenu = self.bilan_markdown()

        with open(chemin, "w", encoding="utf-8") as fichier:
            fichier.write(contenu + "\n")

        return chemin

    # --------------------------------------------------------------- fusion
    def __add__(self, other: "Inventaire") -> "Inventaire":
        """Fusionne deux inventaires dans un nouvel inventaire indépendant."""

        if not isinstance(other, Inventaire):
            return NotImplemented

        resultat = Inventaire()

        for meuble in self.meubles + other.meubles:
            resultat.ajouter(meuble.copy())

        return resultat

    def __iadd__(self, other: "Inventaire") -> "Inventaire":
        """Ajoute les meubles d'un autre inventaire au présent inventaire."""

        if not isinstance(other, Inventaire):
            return NotImplemented

        noms_existants = {m.nom for m in self.meubles}
        noms_ajoutes = [m.nom for m in other.meubles]

        doublons = noms_existants.intersection(noms_ajoutes)

        if doublons or len(noms_ajoutes) != len(set(noms_ajoutes)):
            raise ValueError(
                f"Meubles en double lors de la fusion : "
                f"{sorted(doublons | { n for n in noms_ajoutes if noms_ajoutes.count(n) > 1 })}"
            )

        for meuble in other.meubles:
            self.ajouter(meuble.copy())

        return self
