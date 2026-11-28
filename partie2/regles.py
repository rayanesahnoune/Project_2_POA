"""Règles de mise à jour : quelle couleur l'agent porte-t-il au prochain tour ?
Chaque règle est une fonction regle(agent) -> nouvelle couleur.
En cas d'égalité, l'agent garde sa couleur (aucune couleur n'est favorisée)."""

from agent import AUTRE


def majorite(agent):
    """MAJORITÉ SIMPLE (CM5) : change si, depuis le début, il a vu plus souvent
    l'autre couleur que la sienne. Utilise le COMPTE (tout l'historique)."""
    moi = agent.couleur
    autre = AUTRE[moi]
    if agent.compte[autre] > agent.compte[moi]:
        return autre
    return moi


def hcr(agent):
    """HCR, plus forte récompense cumulée (CM5) : sur ses m dernières rencontres,
    calcule ce que chaque couleur lui AURAIT rapporté, et prend la meilleure.
    Utilise la MÉMOIRE (les m dernières couleurs vues)."""
    moi = agent.couleur
    autre = AUTRE[moi]
    score_moi = sum(agent.gain(moi, vue) for vue in agent.memoire)
    score_autre = sum(agent.gain(autre, vue) for vue in agent.memoire)
    if score_autre > score_moi:
        return autre
    return moi


REGLES = {
    "MAJORITE": majorite,
    "HCR": hcr,
}