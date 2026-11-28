
import argparse
import csv
import os

from moteur import tournament, ranking, evolution
from strategies import POPULATIONS


def print_results(names, h2h, totals):
    rank = ranking(totals)
    print("\n=== Classement ===")
    for pos, (name, score) in enumerate(rank, 1):
        print(f"{pos:>2}. {name:<14} {score:>10.1f}")

    print("\n=== Scores face-à-face (ligne contre colonne) ===")
    w = max(len(n) for n in names) + 2
    print(" " * w + "".join(f"{n:>{w}}" for n in names))
    for a in names:
        row = "".join(
            f"{'-':>{w}}" if h2h[a][b] is None else f"{h2h[a][b]:>{w}.0f}"
            for b in names
        )
        print(f"{a:<{w}}{row}")


def write_csv(names, h2h, totals, outdir, tag):
    os.makedirs(outdir, exist_ok=True)
    rank_path = os.path.join(outdir, f"{tag}_classement.csv")
    with open(rank_path, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["rang", "strategie", "score_total"])
        for pos, (name, score) in enumerate(ranking(totals), 1):
            wr.writerow([pos, name, score])

    h2h_path = os.path.join(outdir, f"{tag}_face_a_face.csv")
    with open(h2h_path, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow([""] + names)
        for a in names:
            wr.writerow([a] + ["" if h2h[a][b] is None else h2h[a][b] for b in names])
    return [rank_path, h2h_path]


def run_evolution(names, h2h, games, generations, outdir, tag):
    history = evolution(names, h2h, games, generations)
    final = sorted(history[-1].items(), key=lambda kv: kv[1], reverse=True)
    print(f"\n=== Sélection : parts de population après {generations} générations ===")
    for name, share in final:
        print(f"{name:<14} {share * 100:6.2f} %")

    csv_path = os.path.join(outdir, f"{tag}_evolution.csv")
    with open(csv_path, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["generation"] + names)
        for g, shares in enumerate(history):
            wr.writerow([g] + [shares[n] for n in names])
    paths = [csv_path]

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(9, 5))
        for n in names:
            ax.plot([h[n] for h in history], label=n, linewidth=2)
        ax.set_xlabel("Génération")
        ax.set_ylabel("Part de la population")
        ax.set_title(f"Sélection – {tag}")
        ax.legend()
        ax.grid(alpha=0.3)
        png = os.path.join(outdir, f"{tag}_evolution.png")
        fig.savefig(png, dpi=120, bbox_inches="tight")
        paths.append(png)
    except ImportError:
        print("(matplotlib absent : pas de graphique, seulement le CSV)")
    return paths


def main():
    p = argparse.ArgumentParser(description="Tournoi de dilemme du prisonnier itéré")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--rounds", type=int, default=200)
    p.add_argument("--repeats", type=int, default=5)
    p.add_argument("--population", choices=sorted(POPULATIONS), default="base")
    p.add_argument("--no-self-play", action="store_true",
                   help="ne pas faire jouer une stratégie contre son double")
    p.add_argument("--noise", type=float, default=0.0,
                   help="probabilité d'inverser chaque coup (ex. 0.05)")
    p.add_argument("--w", type=float, default=None,
                   help="horizon inconnu : probabilité de continuer après chaque tour")
    p.add_argument("--evolution", type=int, default=0, metavar="N",
                   help="sélection sur N générations (dynamique du réplicateur)")
    p.add_argument("--out", default="results")
    args = p.parse_args()

    self_play = not args.no_self_play
    print(f"Population={args.population} seed={args.seed} repeats={args.repeats} "
          f"rounds={'aléatoire (w=%s)' % args.w if args.w is not None else args.rounds} "
          f"noise={args.noise} self_play={self_play}")

    names, h2h, totals, games = tournament(
        POPULATIONS[args.population], rounds=args.rounds, repeats=args.repeats,
        self_play=self_play, seed=args.seed, noise=args.noise, w=args.w,
    )
    print_results(names, h2h, totals)

    tag = f"{args.population}_seed{args.seed}"
    if not self_play:
        tag += "_noself"
    if args.noise:
        tag += f"_noise{args.noise}"
    if args.w is not None:
        tag += f"_w{args.w}"
    paths = write_csv(names, h2h, totals, args.out, tag)
    if args.evolution:
        paths += run_evolution(names, h2h, games, args.evolution, args.out, tag)
    print("\nFichiers écrits :", *paths)


if __name__ == "__main__":
    main()
