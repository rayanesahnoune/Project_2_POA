"""Un agent du jeu du tee-shirt."""

from collections import Counter, deque

ROUGE, BLEU = "R", "B"
AUTRE = {ROUGE: BLEU, BLEU: ROUGE}   # AUTRE["R"] donne "B", et inversement


class Agent:
    def __init__(self, id, couleur, longueur_memoire, rng):
        self.id = id
        self.couleur = couleur                         # couleur portée en ce moment
        self.memoire = deque(maxlen=longueur_memoire)  # les m dernières couleurs vues
        self.compte = Counter()                        # total des couleurs vues depuis le début
        self.dernier_partenaire = None                 # couleur du dernier partenaire
        self.dernier_gain = None                       # gain du dernier tour
        self.rng = rng                                 # hasard propre à l'agent (pour certaines règles)

    def gain(self, couleur_moi, couleur_partenaire):
        """1 si les deux portent la même couleur, 0 sinon."""
        return 1 if couleur_moi == couleur_partenaire else 0

    def observer(self, couleur_partenaire):
        """Enregistre ce que l'agent a vu pendant la rencontre."""
        self.dernier_partenaire = couleur_partenaire
        self.dernier_gain = self.gain(self.couleur, couleur_partenaire)
        self.memoire.append(couleur_partenaire)   # si la mémoire est pleine, la plus ancienne sort
        self.compte[couleur_partenaire] += 1

    def __repr__(self):
        return f"Agent({self.id}, {self.couleur}, memoire={''.join(self.memoire)})"