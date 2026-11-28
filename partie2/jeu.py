"""Le jeu : créer la population, former les paires, jouer un tour, jouer une partie complète."""

import random

from agent import Agent, ROUGE, BLEU
from regles import REGLES


def creer_population(n, memoire, rng):
    """n agents ; chacun porte une couleur tirée au hasard (1 chance sur 2)."""
    return [Agent(i, rng.choice([ROUGE, BLEU]), memoire, random.Random(rng.random()))
            for i in range(n)]


def paires_au_hasard(agents, rng):
    """Mélange la population, puis forme des paires : (1er, 2e), (3e, 4e)...
    Si n est impair, le dernier ne joue pas ce tour."""
    ordre = agents[:]          # copie, pour ne pas changer l'ordre de la vraie liste
    rng.shuffle(ordre)
    return [(ordre[k], ordre[k + 1]) for k in range(0, len(ordre) - 1, 2)]


def jouer_tour(agents, regle, rng):
    """Un tour : 1) tout le monde observe son partenaire, 2) puis tout le monde change."""
    paires = paires_au_hasard(agents, rng)

    # 1) Observation : on lit les deux couleurs AVANT que quiconque ne change.
    for a, b in paires:
        couleur_a, couleur_b = a.couleur, b.couleur
        a.observer(couleur_b)
        b.observer(couleur_a)

    # 2) Mise à jour : chaque agent qui a joué applique sa règle.
    joueurs = [agent for paire in paires for agent in paire]
    for agent in joueurs:
        agent.couleur = regle(agent)


def part_rouge(agents):
    """Part de rouge dans la population. Sert seulement à MESURER, jamais à décider."""
    return sum(1 for a in agents if a.couleur == ROUGE) / len(agents)


def jouer_partie(nom_regle, n, memoire, max_tours, graine, garder_courbe=False):
    """Joue jusqu'à ce que tous portent la même couleur, ou jusqu'à max_tours.
    Renvoie : tours (None si pas de convergence), couleur gagnante,
    part de rouge au départ et à la fin, et la courbe si demandée."""
    rng = random.Random(graine)
    regle = REGLES[nom_regle]
    agents = creer_population(n, memoire, rng)
    rouge_debut = part_rouge(agents)
    courbe = [rouge_debut]

    for t in range(1, max_tours + 1):
        jouer_tour(agents, regle, rng)
        p = part_rouge(agents)
        if garder_courbe:
            courbe.append(p)
        if p == 0.0 or p == 1.0:                 # tout le monde a la même couleur
            gagnante = ROUGE if p == 1.0 else BLEU
            return {"tours": t, "gagnante": gagnante,
                    "rouge_debut": rouge_debut, "rouge_fin": p, "courbe": courbe}

    return {"tours": None, "gagnante": None,
            "rouge_debut": rouge_debut, "rouge_fin": part_rouge(agents), "courbe": courbe}