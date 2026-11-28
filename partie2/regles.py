"""Règles de mise à jour : à partir de ce que l'agent a observé, quelle couleur porter au prochain tour ?

Chaque règle est une fonction regle(agent) -> nouvelle couleur.
En cas d'égalité, l'agent GARDE sa couleur : aucune couleur n'est favorisée.

⚠️ Vérifier que MAJORITE et HCR correspondent EXACTEMENT aux diapositives du cours 5.
"""

from agent import AUTRE


# ---------------------------------------------------------------- règles du cours

def majorite(agent):
    """MAJORITÉ SIMPLE (cours 5 ; Walker et Wooldridge, 1995).
    L'agent change de couleur s'il a vu, depuis le début, PLUS de partenaires de l'autre couleur
    que de la sienne. Il compte TOUT son historique (pas de limite de mémoire)."""
    moi, autre = agent.couleur, AUTRE[agent.couleur]
    if agent.compte[autre] > agent.compte[moi]:
        return autre
    return moi


def hcr(agent):
    """PLUS FORTE RÉCOMPENSE CUMULÉE, HCR (cours 5 ; Shoham et Tennenholtz).
    Sur ses m dernières rencontres, l'agent calcule ce que chaque couleur lui AURAIT rapporté :
    porter la couleur c aurait gagné à chaque fois que le partenaire portait c.
    Il prend la couleur qui aurait rapporté le plus. Avec des gains symétriques, ça revient
    à prendre la couleur la plus vue dans sa mémoire récente."""
    moi, autre = agent.couleur, AUTRE[agent.couleur]
    score_moi = sum(agent.gain(moi, vue) for vue in agent.memoire)
    score_autre = sum(agent.gain(autre, vue) for vue in agent.memoire)
    if score_autre > score_moi:
        return autre
    return moi


# ---------------------------------------------------------------- règles absentes du cours (étape 2)

def imitation(agent):
    """IMITATION : prend la couleur de son dernier partenaire.
    (S'il n'a pas joué ce tour, il garde sa couleur.)"""
    if agent.dernier_partenaire is None:
        return agent.couleur
    return agent.dernier_partenaire


PROBA_IMITATION = 0.5


def imitation_proba(agent):
    """IMITATION HÉSITANTE (modèle de l'électeur, « voter model ») : si le dernier partenaire
    portait l'autre couleur, l'agent la copie avec probabilité 0,5, sinon il garde la sienne.
    Le hasard casse l'échange systématique des couleurs de IMITATION."""
    if agent.dernier_partenaire is None or agent.dernier_partenaire == agent.couleur:
        return agent.couleur
    if agent.rng.random() < PROBA_IMITATION:
        return agent.dernier_partenaire
    return agent.couleur


def wsls(agent):
    """GAGNER-RESTER / PERDRE-CHANGER (Win-Stay Lose-Shift, comme PAVLOV en partie 1 ;
    Nowak et Sigmund, 1993). S'il a gagné au dernier tour, il garde sa couleur ; sinon il change."""
    if agent.dernier_gain is None:
        return agent.couleur
    if agent.dernier_gain > 0:
        return agent.couleur
    return AUTRE[agent.couleur]


SEUIL = 0.7


def seuil(agent):
    """SEUIL (majorité qualifiée) : change seulement si au moins 70 % de sa mémoire récente
    est de l'autre couleur. Plus prudent que HCR : il ne bouge pas pour une faible majorité."""
    if not agent.memoire:
        return agent.couleur
    autre = AUTRE[agent.couleur]
    part_autre = sum(1 for vue in agent.memoire if vue == autre) / len(agent.memoire)
    if part_autre >= SEUIL:
        return autre
    return agent.couleur


REGLES = {
    "MAJORITE": majorite,
    "HCR": hcr,
    "IMITATION": imitation,
    "IMITATION_PROBA": imitation_proba,
    "WSLS": wsls,
    "SEUIL": seuil,
}
