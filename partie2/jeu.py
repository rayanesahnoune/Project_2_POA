"""Le jeu : une population, la formation des paires, un tour, une partie complète."""

import math
import random

from agent import Agent, ROUGE, BLEU
from regles import REGLES


class Config:
    """Tous les paramètres d'une partie (le protocole)."""

    def __init__(self, n=100, memoire=10, max_tours=1000, tetus=0.0, couleur_tetus="R",
                 reset=0, voisinage=False, asym=None):
        self.n = n                    # taille de la population
        self.memoire = memoire        # longueur de la mémoire (m dernières rencontres)
        self.max_tours = max_tours    # au-delà : la partie « ne converge pas »
        self.tetus = tetus            # part d'agents têtus (étape 3), ex : 0.05
        self.couleur_tetus = couleur_tetus  # "R", "B" ou "hasard"
        self.reset = reset            # mémoire remise à zéro tous les `reset` tours (0 = jamais)
        self.voisinage = voisinage    # True : agents sur une grille, appariés à un voisin libre
        self.asym = asym              # None : gains symétriques ; sinon part d'agents qui préfèrent ROUGE


def creer_population(config, rng):
    """Chaque agent porte une couleur tirée au hasard (1 chance sur 2)."""
    agents = []
    n_tetus = round(config.tetus * config.n)
    for i in range(config.n):
        couleur = rng.choice([ROUGE, BLEU])
        tetu = i < n_tetus
        if tetu and config.couleur_tetus in (ROUGE, BLEU):
            couleur = config.couleur_tetus
        preferee = None
        if config.asym is not None:
            preferee = ROUGE if rng.random() < config.asym else BLEU
        agents.append(Agent(i, couleur, config.memoire, random.Random(rng.random()), tetu, preferee))
    rng.shuffle(agents)  # les têtus ne sont pas tous au même endroit de la grille
    return agents


def paires_au_hasard(agents, rng):
    """Mélange la population et forme des paires (0,1), (2,3)…
    Si N est impair, le dernier agent ne joue pas ce tour."""
    ordre = agents[:]
    rng.shuffle(ordre)
    return [(ordre[k], ordre[k + 1]) for k in range(0, len(ordre) - 1, 2)]


def voisins(index, cote):
    """Indices des 4 voisins (haut, bas, gauche, droite) sur une grille cote × cote, sans bords qui se rejoignent."""
    ligne, col = divmod(index, cote)
    resultat = []
    for dl, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        l, c = ligne + dl, col + dc
        if 0 <= l < cote and 0 <= c < cote:
            resultat.append(l * cote + c)
    return resultat


def paires_voisinage(agents, rng):
    """Les agents sont sur une grille (agent k à la case k). Dans un ordre au hasard,
    chaque agent encore libre est apparié à un voisin libre tiré au hasard.
    Un agent sans voisin libre ne joue pas ce tour."""
    cote = math.isqrt(len(agents))
    libre = [True] * len(agents)
    ordre = list(range(len(agents)))
    rng.shuffle(ordre)
    paires = []
    for i in ordre:
        if not libre[i]:
            continue
        candidats = [j for j in voisins(i, cote) if libre[j]]
        if not candidats:
            continue
        j = rng.choice(candidats)
        libre[i] = libre[j] = False
        paires.append((agents[i], agents[j]))
    return paires


def jouer_tour(agents, regle, config, rng, numero_tour):
    """Un tour complet. Renvoie le gain moyen des agents qui ont joué."""
    paires = paires_voisinage(agents, rng) if config.voisinage else paires_au_hasard(agents, rng)

    # 1) Observation : TOUT LE MONDE observe avant que quiconque ne change
    #    (sinon l'ordre des agents influencerait le résultat).
    for a in agents:
        a.pas_joue()
    for a, b in paires:
        ca, cb = a.couleur, b.couleur
        a.observer(cb)
        b.observer(ca)

    # 2) Mise à jour : chaque agent qui a joué applique sa règle (sauf les têtus).
    for a in agents:
        if a.tetu or a.dernier_partenaire is None:
            continue
        a.couleur = regle(a)

    # 3) Mémoire remise à zéro de temps en temps (modification « mémoire »).
    if config.reset and numero_tour % config.reset == 0:
        for a in agents:
            a.oublier()

    gains = [a.dernier_gain for a in agents if a.dernier_gain is not None]
    return sum(gains) / len(gains) if gains else 0.0


def part_rouge(agents):
    return sum(1 for a in agents if a.couleur == ROUGE) / len(agents)


def jouer_partie(nom_regle, config, graine, garder_courbe=False):
    """Joue une partie jusqu'à ce que tous portent la même couleur, ou jusqu'à max_tours.

    Renvoie un dictionnaire :
      tours        : nombre de tours pour converger (None si pas de convergence)
      gagnante     : couleur de tous à la convergence (None sinon)
      rouge_debut  : part de rouge au tour 0
      rouge_fin    : part de rouge à la fin
      courbe       : part de rouge à chaque tour (si garder_courbe)
    """
    if config.voisinage and math.isqrt(config.n) ** 2 != config.n:
        raise ValueError("Avec --voisinage, N doit être un carré (ex : 100 pour une grille 10 × 10)")
    rng = random.Random(graine)
    regle = REGLES[nom_regle]
    agents = creer_population(config, rng)
    rouge_debut = part_rouge(agents)
    courbe = [rouge_debut]

    for t in range(1, config.max_tours + 1):
        jouer_tour(agents, regle, config, rng, t)
        p = part_rouge(agents)
        if garder_courbe:
            courbe.append(p)
        if p == 0.0 or p == 1.0:
            return {"tours": t, "gagnante": ROUGE if p == 1.0 else BLEU,
                    "rouge_debut": rouge_debut, "rouge_fin": p, "courbe": courbe}
    return {"tours": None, "gagnante": None, "rouge_debut": rouge_debut,
            "rouge_fin": part_rouge(agents), "courbe": courbe}
