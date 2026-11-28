"""Lance les expériences du jeu du tee-shirt et affiche / sauvegarde les résultats.

Exemples :
  python main.py --regles HCR MAJORITE                          # étape 1
  python main.py --regles HCR MAJORITE IMITATION WSLS SEUIL     # étape 2
  python main.py --regles HCR --tetus 0.05                      # étape 3 : têtus
  python main.py --regles HCR --voisinage                       # étape 3 : voisinage
"""

import argparse
import csv
import os

from experiences import experience, resume
from jeu import Config, jouer_partie
from regles import REGLES


def fmt(x, dec=1):
    return "-" if x is None else f"{x:.{dec}f}"


def main():
    p = argparse.ArgumentParser(description="Jeu du tee-shirt : émergence d'une convention")
    p.add_argument("--regles", nargs="+", default=["HCR", "MAJORITE"], choices=sorted(REGLES))
    p.add_argument("--n", type=int, default=100, help="taille de la population")
    p.add_argument("--memoire", type=int, default=10, help="longueur de la mémoire m")
    p.add_argument("--max-tours", type=int, default=1000)
    p.add_argument("--graines", type=int, default=200, help="nombre de graines (une partie par graine)")
    p.add_argument("--graine-depart", type=int, default=0, help="première graine (graines = départ, départ+1, ...)")
    # étape 3
    p.add_argument("--tetus", type=float, default=0.0, help="part d'agents têtus, ex : 0.05")
    p.add_argument("--couleur-tetus", default="R", choices=["R", "B", "hasard"])
    p.add_argument("--reset", type=int, default=0, help="mémoire remise à zéro tous les N tours (0 = jamais)")
    p.add_argument("--voisinage", action="store_true", help="agents sur une grille (N doit être un carré)")
    p.add_argument("--asym", type=float, default=None,
                   help="gains asymétriques : part des agents qui préfèrent ROUGE (ex : 0.5)")
    # sorties
    p.add_argument("--courbes", type=int, default=0, help="tracer la part de rouge pour les K premières graines")
    p.add_argument("--out", default="resultats")
    p.add_argument("--tag", default="", help="suffixe ajouté au nom des fichiers")
    args = p.parse_args()

    config = Config(n=args.n, memoire=args.memoire, max_tours=args.max_tours, tetus=args.tetus,
                    couleur_tetus=args.couleur_tetus, reset=args.reset,
                    voisinage=args.voisinage, asym=args.asym)
    graines = list(range(args.graine_depart, args.graine_depart + args.graines))

    print(f"N={args.n} mémoire={args.memoire} max_tours={args.max_tours} "
          f"graines={graines[0]}..{graines[-1]} têtus={args.tetus} ({args.couleur_tetus}) "
          f"reset={args.reset} voisinage={args.voisinage} asym={args.asym}")

    entetes = ["regle", "parties", "converge_pct", "tours_moyen", "tours_median", "tours_max",
               "rouge_gagne_pct", "majorite_initiale_gagne_pct", "rouge_fin_moyen_pct"]
    lignes = []
    print(f"\n{'Règle':<16} {'converge':>9} {'tours moy':>10} {'médiane':>8} {'max':>6} "
          f"{'rouge gagne':>12} {'majo. init. gagne':>18} {'rouge fin':>10}")
    for nom in args.regles:
        r = resume(experience(nom, config, graines))
        lignes.append([nom] + [r[k] for k in entetes[1:]])
        print(f"{nom:<16} {fmt(r['converge_pct']):>8}% {fmt(r['tours_moyen']):>10} "
              f"{fmt(r['tours_median']):>8} {fmt(r['tours_max'], 0):>6} "
              f"{fmt(r['rouge_gagne_pct']):>11}% {fmt(r['majorite_initiale_gagne_pct']):>17}% "
              f"{fmt(r['rouge_fin_moyen_pct']):>9}%")

    os.makedirs(args.out, exist_ok=True)
    nom_fichier = "_".join(args.regles) + (f"_{args.tag}" if args.tag else "")
    chemin = os.path.join(args.out, f"{nom_fichier}.csv")
    with open(chemin, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(entetes)
        w.writerows(lignes)
    print(f"\nCSV : {chemin}")

    if args.courbes:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except ImportError:
            print("(matplotlib absent : pas de graphique)")
            return
        fig, axes = plt.subplots(1, len(args.regles), figsize=(5 * len(args.regles), 4),
                                 squeeze=False, sharey=True)
        for ax, nom in zip(axes[0], args.regles):
            for g in graines[:args.courbes]:
                res = jouer_partie(nom, config, g, garder_courbe=True)
                ax.plot(res["courbe"], label=f"graine {g}")
            ax.set_title(nom)
            ax.set_xlabel("Tour")
            ax.grid(alpha=0.3)
        axes[0][0].set_ylabel("Part de rouge")
        axes[0][-1].legend(fontsize=7)
        png = os.path.join(args.out, f"{nom_fichier}_courbes.png")
        fig.savefig(png, dpi=110, bbox_inches="tight")
        print(f"Graphique : {png}")


if __name__ == "__main__":
    main()
