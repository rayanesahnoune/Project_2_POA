"""Tests unitaires. Lancer : python -m unittest -v"""

import random
import unittest

from agent import Agent, ROUGE, BLEU
from jeu import Config, jouer_partie, paires_au_hasard, paires_voisinage, voisins, creer_population
from regles import hcr, majorite, imitation, wsls, seuil


def agent_avec(couleur, vues, m=10):
    """Crée un agent qui a déjà vu la liste de couleurs `vues`."""
    a = Agent(0, couleur, m, random.Random(0))
    for v in vues:
        a.observer(v)
    return a


class TestRegles(unittest.TestCase):
    def test_hcr_change_si_autre_couleur_plus_vue(self):
        # Mémoire R, R, B : rouge aurait rapporté 2, bleu 1 -> un agent BLEU passe ROUGE.
        self.assertEqual(hcr(agent_avec(BLEU, "RRB")), ROUGE)

    def test_hcr_garde_en_cas_egalite(self):
        self.assertEqual(hcr(agent_avec(BLEU, "RB")), BLEU)
        self.assertEqual(hcr(agent_avec(ROUGE, "RB")), ROUGE)

    def test_hcr_ne_regarde_que_les_m_dernieres(self):
        # m = 3 : la mémoire ne garde que B, B, R -> un agent ROUGE passe BLEU,
        # même s'il a vu beaucoup de rouge avant.
        self.assertEqual(hcr(agent_avec(ROUGE, "RRRRRBBR", m=3)), BLEU)

    def test_majorite_compte_tout_l_historique(self):
        # Même suite : en tout 6 R et 2 B -> la majorité simple reste ROUGE.
        self.assertEqual(majorite(agent_avec(ROUGE, "RRRRRBBR", m=3)), ROUGE)

    def test_imitation(self):
        self.assertEqual(imitation(agent_avec(ROUGE, "RRB")), BLEU)

    def test_imitation_conserve_la_part_de_rouge(self):
        # Deux agents de couleurs différentes s'imitent : ils échangent leurs couleurs,
        # donc la part de rouge ne change jamais -> pas de convergence.
        res = jouer_partie("IMITATION", Config(n=50, max_tours=100), 3, garder_courbe=True)
        self.assertEqual(len(set(res["courbe"])), 1)

    def test_wsls(self):
        self.assertEqual(wsls(agent_avec(ROUGE, "R")), ROUGE)  # gagné -> garde
        self.assertEqual(wsls(agent_avec(ROUGE, "B")), BLEU)   # perdu -> change

    def test_seuil(self):
        self.assertEqual(seuil(agent_avec(ROUGE, "BBR")), ROUGE)    # 67 % < 70 % -> garde
        self.assertEqual(seuil(agent_avec(ROUGE, "BBBR")), BLEU)    # 75 % >= 70 % -> change

    def test_hcr_gains_asymetriques(self):
        # Préfère ROUGE : vu R, B, B -> rouge aurait rapporté 2 × 1 = 2, bleu 1 × 2 = 2 : égalité, il garde.
        a = Agent(0, BLEU, 10, random.Random(0), preferee=ROUGE)
        for v in "RBB":
            a.observer(v)
        self.assertEqual(hcr(a), BLEU)


class TestJeu(unittest.TestCase):
    def test_chacun_joue_une_fois(self):
        agents = creer_population(Config(n=10), random.Random(1))
        paires = paires_au_hasard(agents, random.Random(2))
        ids = [a.id for p in paires for a in p]
        self.assertEqual(sorted(ids), list(range(10)))

    def test_impair_un_agent_ne_joue_pas(self):
        agents = creer_population(Config(n=7), random.Random(1))
        self.assertEqual(len(paires_au_hasard(agents, random.Random(2))), 3)

    def test_voisins_grille(self):
        # Grille 3 × 3 : le coin 0 a 2 voisins, le centre 4 en a 4.
        self.assertEqual(sorted(voisins(0, 3)), [1, 3])
        self.assertEqual(sorted(voisins(4, 3)), [1, 3, 5, 7])

    def test_voisinage_paires_entre_voisins(self):
        agents = creer_population(Config(n=16), random.Random(1))
        for a, b in paires_voisinage(agents, random.Random(3)):
            i, j = agents.index(a), agents.index(b)
            self.assertIn(j, voisins(i, 4))

    def test_reproductible(self):
        c = Config(n=50)
        self.assertEqual(jouer_partie("HCR", c, 7), jouer_partie("HCR", c, 7))

    def test_tetus_ne_changent_jamais(self):
        c = Config(n=20, tetus=0.25, couleur_tetus=ROUGE, max_tours=50)
        res = jouer_partie("HCR", c, 1)
        self.assertGreater(res["rouge_fin"], 0)  # les 5 têtus rouges sont toujours là

    def test_convergence_detectee(self):
        res = jouer_partie("HCR", Config(n=20), 0)
        if res["tours"] is not None:
            self.assertIn(res["rouge_fin"], (0.0, 1.0))


if __name__ == "__main__":
    unittest.main()
