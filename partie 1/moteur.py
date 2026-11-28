

import random

# Matrice des gains (cours 4) : (gain joueur 1, gain joueur 2)
PAYOFFS = {
    ("C", "C"): (3, 3),
    ("C", "D"): (0, 5),
    ("D", "C"): (5, 0),
    ("D", "D"): (2, 2),
}

FLIP = {"C": "D", "D": "C"}


def match(s1, s2, rounds=200, noise=0.0, noise_rng=None):
   
    if noise > 0 and noise_rng is None:
        raise ValueError("noise > 0 demande un noise_rng (reproductibilité)")
    s1.reset()
    s2.reset()
    h1, h2 = [], []
    score1 = score2 = 0
    for _ in range(rounds):

        m1 = s1.play(list(h1), list(h2))
        m2 = s2.play(list(h2), list(h1))
        if m1 not in ("C", "D") or m2 not in ("C", "D"):
            raise ValueError(f"Coup invalide : {s1.name}={m1!r}, {s2.name}={m2!r}")
        if noise > 0:
            if noise_rng.random() < noise:
                m1 = FLIP[m1]
            if noise_rng.random() < noise:
                m2 = FLIP[m2]
        g1, g2 = PAYOFFS[(m1, m2)]
        score1 += g1
        score2 += g2
        h1.append(m1)
        h2.append(m2)
    return score1, score2, h1, h2


def draw_length(rng, w, max_rounds=10_000):
  
    n = 1
    while n < max_rounds and rng.random() < w:
        n += 1
    return n


def tournament(strategies, rounds=200, repeats=5, self_play=True, seed=0,
               noise=0.0, w=None):
   
    master = random.Random(seed)
    names = [cls.name for cls in strategies]
    if len(set(names)) != len(names):
        raise ValueError("Deux stratégies ont le même nom")
    h2h = {a: {b: None for b in names} for a in names}
    games = {a: {b: 0 for b in names} for a in names}

    n = len(strategies)
    for i in range(n):
        for j in range(i, n):
            if i == j and not self_play:
                continue
            ca, cb = strategies[i], strategies[j]
            tot_a = tot_b = 0
            n_rounds = 0
            for _ in range(repeats):
                pa = ca(random.Random(master.randrange(2**32)))
                pb = cb(random.Random(master.randrange(2**32)))
               
                noise_rng = random.Random(master.randrange(2**32)) if noise > 0 else None
                length = draw_length(master, w) if w is not None else rounds
                sa, sb, _, _ = match(pa, pb, length, noise, noise_rng)
                tot_a += sa
                tot_b += sb
                n_rounds += length
            games[ca.name][cb.name] = games[cb.name][ca.name] = n_rounds
            if i == j:
                h2h[ca.name][ca.name] = (tot_a + tot_b) / 2
            else:
                h2h[ca.name][cb.name] = tot_a
                h2h[cb.name][ca.name] = tot_b

    totals = {a: sum(v for v in h2h[a].values() if v is not None) for a in names}
    return names, h2h, totals, games


def ranking(totals):

    return sorted(totals.items(), key=lambda kv: kv[1], reverse=True)


def evolution(names, h2h, games, generations=100):
    

    for a in names:
        if h2h[a][a] is None:
            raise ValueError("La sélection nécessite le self-play")
    A = {a: {b: h2h[a][b] / games[a][b] for b in names} for a in names}
    shares = {a: 1 / len(names) for a in names}
    history = [dict(shares)]
    for _ in range(generations):
        fit = {a: sum(shares[b] * A[a][b] for b in names) for a in names}
        mean = sum(shares[a] * fit[a] for a in names)
        shares = {a: shares[a] * fit[a] / mean for a in names}
        history.append(dict(shares))
    return history
