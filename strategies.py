
class Strategy:
    name = "BASE"

    def __init__(self, rng):
        self.rng = rng
        self.reset()

    def reset(self):
        pass

    def play(self, my_history, opp_history):
        raise NotImplementedError


class AllD(Strategy):
    """Trahit toujours."""
    name = "ALL-D"

    def play(self, my_history, opp_history):
        return "D"


class Random(Strategy):
    """Coopère avec probabilité p = 0.5."""
    name = "RANDOM"
    p = 0.5

    def play(self, my_history, opp_history):
        return "C" if self.rng.random() < self.p else "D"


class TitForTat(Strategy):
    """Coopère au premier tour, puis copie le dernier coup de l'adversaire."""
    name = "TIT-FOR-TAT"

    def play(self, my_history, opp_history):
        return opp_history[-1] if opp_history else "C"


class Joss(Strategy):
    """TIT-FOR-TAT sournois : quand il devrait coopérer, trahit quand même
    avec probabilité 10 %."""
    name = "JOSS"
    sneak = 0.1

    def play(self, my_history, opp_history):
        if opp_history and opp_history[-1] == "D":
            return "D"
        return "D" if self.rng.random() < self.sneak else "C"


class Tester(Strategy):
    """Sonde l'adversaire : trahit au tour 1.
    - Si l'adversaire trahit un jour, s'excuse (coopère une fois) puis joue
      TIT-FOR-TAT jusqu'à la fin.
    - Sinon, coopère aux tours 2 et 3, puis trahit un tour sur deux
      (tours 4, 6, 8, ...).
    """
    name = "TESTER"

    def reset(self):
        self.retaliated = False  # l'adversaire a-t-il déjà trahi ?
        self.apologized = False

    def play(self, my_history, opp_history):
        t = len(my_history)  # index du tour courant (0 = premier tour)
        if t == 0:
            return "D"
        if not self.retaliated and "D" in opp_history:
            self.retaliated = True
        if self.retaliated:
            if not self.apologized:
                self.apologized = True
                return "C"  # excuse
            return opp_history[-1]  # TIT-FOR-TAT
        if t in (1, 2):
            return "C"
        return "D" if t % 2 == 1 else "C"  # tours 4, 6, 8... (t = 3, 5, 7...)


# ---------- Étape 2 : stratégies absentes du cours ----------

class Pavlov(Strategy):
    """Win-Stay, Lose-Shift (Nowak & Sigmund, 1993).
    Coopère au premier tour. Ensuite : si le dernier tour a bien rapporté
    (3 ou 5 points), rejoue le même coup ; sinon (0 ou 2), change de coup.
    Équivalent : coopère si les deux joueurs ont fait le même coup au tour précédent.
    """
    name = "PAVLOV"

    def play(self, my_history, opp_history):
        if not my_history:
            return "C"
        return "C" if my_history[-1] == opp_history[-1] else "D"


class GenerousTFT(Strategy):
    """TIT-FOR-TAT généreux (Nowak & Sigmund, 1992).
    Comme TIT-FOR-TAT, mais quand l'adversaire a trahi, pardonne (coopère)
    avec probabilité 10 %.
    """
    name = "GENEROUS-TFT"
    generosity = 0.1

    def play(self, my_history, opp_history):
        if not opp_history or opp_history[-1] == "C":
            return "C"
        return "C" if self.rng.random() < self.generosity else "D"


BASE = [AllD, Random, TitForTat, Tester, Joss]
ETENDUE = BASE + [Pavlov, GenerousTFT]

POPULATIONS = {
    "base": BASE,
    "etendue": ETENDUE,
}
