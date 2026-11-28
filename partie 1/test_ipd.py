"""Tests unitaires. Lancer : python -m unittest -v"""

import random
import unittest

from moteur import match, tournament
from strategies import AllD, Random, TitForTat, Tester, Joss, BASE


def mk(cls, seed=0):
    return cls(random.Random(seed))


class TestMatch(unittest.TestCase):
    def test_tft_vs_alld(self):
        # Tour 1 : C/D -> 0/5, puis 199 tours D/D -> 2/2
        # TFT = 0 + 199*2 = 398 ; ALL-D = 5 + 199*2 = 403
        s1, s2, _, _ = match(mk(TitForTat), mk(AllD), 200)
        self.assertEqual((s1, s2), (398, 403))

    def test_tft_vs_tft(self):
        s1, s2, _, _ = match(mk(TitForTat), mk(TitForTat), 200)
        self.assertEqual((s1, s2), (600, 600))

    def test_alld_vs_alld(self):
        s1, s2, _, _ = match(mk(AllD), mk(AllD), 200)
        self.assertEqual((s1, s2), (400, 400))

    def test_tester_exploits_tft_free_partner(self):
        # Contre un coopérateur inconditionnel, TESTER : D puis C, C, D répété
        class AllC(TitForTat):
            name = "ALL-C"
            def play(self, m, o):
                return "C"
        _, _, h, _ = match(mk(Tester), mk(AllC), 8)
        self.assertEqual("".join(h), "DCCDCCDC")

    def test_tester_vs_tft(self):
        # TFT riposte au tour 2 -> TESTER s'excuse au tour 3 puis TFT.
        # T1 : TESTER D / TFT C ; T2 : C / D (TFT riposte) ;
        # T3 : TESTER passe en TFT et copie le D ; TFT copie le C -> écho sans fin.
        _, _, ht, hf = match(mk(Tester), mk(TitForTat), 6)
        self.assertEqual("".join(ht), "DCDCDC")
        self.assertEqual("".join(hf), "CDCDCD")

    def test_random_deterministic(self):
        _, _, h1, _ = match(mk(Random, 7), mk(AllD), 50)
        _, _, h2, _ = match(mk(Random, 7), mk(AllD), 50)
        self.assertEqual(h1, h2)

    def test_joss_defects_sometimes(self):
        _, _, h, _ = match(mk(Joss, 1), mk(TitForTat), 200)
        self.assertIn("D", h)


class TestNewStrategies(unittest.TestCase):
    def test_pavlov_vs_alld(self):
        # Pavlov alterne C, D, C, D... contre ALL-D (perd 0, change, gagne 2... perd, change)
        from strategies import Pavlov
        _, _, h, _ = match(mk(Pavlov), mk(AllD), 6)
        self.assertEqual("".join(h), "CDCDCD")

    def test_pavlov_vs_tft(self):
        from strategies import Pavlov
        s1, s2, _, _ = match(mk(Pavlov), mk(TitForTat), 200)
        self.assertEqual((s1, s2), (600, 600))

    def test_tf2t_forgives_single_defection(self):
        from strategies import TitForTwoTats
        class OneD(TitForTat):
            name = "ONE-D"
            def play(self, m, o):
                return "D" if len(m) == 1 else "C"
        _, _, h, _ = match(mk(TitForTwoTats), mk(OneD), 5)
        self.assertEqual("".join(h), "CCCCC")

    def test_tf2t_vs_alld(self):
        from strategies import TitForTwoTats
        _, _, h, _ = match(mk(TitForTwoTats), mk(AllD), 5)
        self.assertEqual("".join(h), "CCDDD")


class TestModifications(unittest.TestCase):
    def test_noise_zero_unchanged(self):
        s1, s2, _, _ = match(mk(TitForTat), mk(AllD), 200, 0.0, random.Random(0))
        self.assertEqual((s1, s2), (398, 403))

    def test_noise_one_flips_everything(self):
        # Avec noise=1, ALL-D joue toujours C et TFT... copie les C -> tout C après inversion
        _, _, h1, h2 = match(mk(AllD), mk(AllD), 10, 1.0, random.Random(0))
        self.assertEqual(set(h1), {"C"})
        self.assertEqual(set(h2), {"C"})

    def test_noise_needs_rng(self):
        with self.assertRaises(ValueError):
            match(mk(AllD), mk(AllD), 10, 0.05)

    def test_horizon_length_mean(self):
        from moteur import draw_length
        rng = random.Random(0)
        lengths = [draw_length(rng, 0.99) for _ in range(5000)]
        mean = sum(lengths) / len(lengths)
        self.assertAlmostEqual(mean, 100, delta=5)  # 1 / (1 - 0.99) = 100

    def test_evolution_shares_sum_to_one(self):
        from moteur import evolution
        names, h2h, _, games = tournament(BASE, seed=0)
        hist = evolution(names, h2h, games, 50)
        for shares in hist:
            self.assertAlmostEqual(sum(shares.values()), 1.0)

    def test_evolution_alld_vs_tft_only(self):
        # Population TFT + ALL-D : TFT gagne 3/tour contre lui-même, ALL-D 2 -> TFT envahit
        from moteur import evolution
        names, h2h, _, games = tournament([TitForTat, AllD], seed=0)
        hist = evolution(names, h2h, games, 200)
        self.assertGreater(hist[-1]["TIT-FOR-TAT"], 0.99)


class TestTournament(unittest.TestCase):
    def test_reproducible(self):
        r1 = tournament(BASE, seed=42)
        r2 = tournament(BASE, seed=42)
        self.assertEqual(r1, r2)

    def test_self_play_flag(self):
        names, h2h, _, _ = tournament(BASE, self_play=False, seed=1)
        for n in names:
            self.assertIsNone(h2h[n][n])

    def test_deterministic_pair_score(self):
        _, h2h, _, _ = tournament([TitForTat, AllD], repeats=5, seed=0)
        self.assertEqual(h2h["TIT-FOR-TAT"]["ALL-D"], 5 * 398)
        self.assertEqual(h2h["ALL-D"]["TIT-FOR-TAT"], 5 * 403)


if __name__ == "__main__":
    unittest.main()
