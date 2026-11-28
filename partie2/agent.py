"""Un agent du jeu du tee-shirt."""

from collections import Counter, deque

ROUGE, BLEU = "R", "B"
AUTRE = {ROUGE: BLEU, BLEU: ROUGE}


class Agent:
    """Un agent porte un tee-shirt (ROUGE ou BLEU) et se souvient de ce qu'il a vu.

    Attributs :
      id        : numéro de l'agent
      couleur   : couleur portée en ce moment
      memoire   : les m dernières couleurs vues chez ses partenaires (la plus ancienne sort)
      compte    : nombre total de fois où il a vu chaque couleur depuis le début
      dernier_partenaire : couleur du dernier partenaire (None s'il n'a pas joué)
      dernier_gain       : gain du dernier tour (None s'il n'a pas joué)
      tetu      : s'il est têtu, il ne change jamais de couleur (étape 3)
      preferee  : couleur préférée si les gains sont asymétriques (étape 3), sinon None
      rng       : générateur aléatoire de l'agent (pour les règles qui tirent au hasard)
    """

    def __init__(self, id, couleur, longueur_memoire, rng, tetu=False, preferee=None):
        self.id = id
        self.couleur = couleur
        self.memoire = deque(maxlen=longueur_memoire)
        self.compte = Counter()
        self.dernier_partenaire = None
        self.dernier_gain = None
        self.tetu = tetu
        self.preferee = preferee
        self.rng = rng

    def gain(self, couleur_moi, couleur_partenaire):
        """Gain d'une rencontre : 0 si les couleurs diffèrent.
        Gains symétriques : 1 si même couleur.
        Gains asymétriques (cinéma / concert) : 2 si on se retrouve sur sa couleur préférée, 1 sur l'autre."""
        if couleur_moi != couleur_partenaire:
            return 0
        if self.preferee is None:
            return 1
        return 2 if couleur_moi == self.preferee else 1

    def observer(self, couleur_partenaire):
        """Enregistre la couleur vue chez le partenaire et le gain obtenu."""
        self.dernier_partenaire = couleur_partenaire
        self.dernier_gain = self.gain(self.couleur, couleur_partenaire)
        self.memoire.append(couleur_partenaire)
        self.compte[couleur_partenaire] += 1

    def pas_joue(self):
        """Ce tour, l'agent n'a pas eu de partenaire (voisinage) : rien de nouveau à observer."""
        self.dernier_partenaire = None
        self.dernier_gain = None

    def oublier(self):
        """Remet la mémoire à zéro (modification « mémoire » de l'étape 3)."""
        self.memoire.clear()
        self.compte.clear()

    def __repr__(self):
        return f"Agent({self.id}, {self.couleur}, mem={''.join(self.memoire)})"
