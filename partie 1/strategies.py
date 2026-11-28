

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
    name = "TIT-FOR-TAT"

    def play(self, my_history, opp_history):
        return opp_history[-1] if opp_history else "C"


class Joss(Strategy):
  
    name = "JOSS"
    sneak = 0.1

    def play(self, my_history, opp_history):
        if opp_history and opp_history[-1] == "D":
            return "D"
        return "D" if self.rng.random() < self.sneak else "C"


class Tester(Strategy):
 
    name = "TESTER"

    def play(self, my_history, opp_history):
        t = len(my_history)  # index du tour courant (0 = premier tour)
        if t == 0:
            return "D"
        if "D" in opp_history:          # l'adversaire a riposté
            return opp_history[-1]      # TIT-FOR-TAT
        return "D" if t % 3 == 0 else "C"   # tours 2,3,4 = C,C,D ; 5,6,7 = C,C,D ...


# ---------- Étape 2 ----------

class Pavlov(Strategy):
    
    name = "PAVLOV"

    def play(self, my_history, opp_history):
        if not my_history:
            return "C"
        return "C" if my_history[-1] == opp_history[-1] else "D"


class TitForTwoTats(Strategy):
 
    name = "TF2T"

    def play(self, my_history, opp_history):
        if len(opp_history) >= 2 and opp_history[-1] == "D" and opp_history[-2] == "D":
            return "D"
        return "C"


BASE = [AllD, Random, TitForTat, Tester, Joss]
ETENDUE = BASE + [Pavlov, TitForTwoTats]

POPULATIONS = {
    "base": BASE,
    "etendue": ETENDUE,
}
