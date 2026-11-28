"""Lance beaucoup de parties (une par graine) et résume les résultats."""

import statistics

from agent import ROUGE
from jeu import jouer_partie


def experience(nom_regle, config, graines):
    """Une partie par graine, avec les mêmes graines pour toutes les règles (comparaison juste)."""
    return [jouer_partie(nom_regle, config, g) for g in graines]


def resume(resultats):
    """Mesures demandées : tours pour converger, % de convergence, couleur gagnante."""
    converges = [r for r in resultats if r["tours"] is not None]
    tours = [r["tours"] for r in converges]
    rouges = [r for r in converges if r["gagnante"] == ROUGE]
    # La couleur gagnante est-elle celle qui était majoritaire au départ ?
    avec_majorite = [r for r in converges if r["rouge_debut"] != 0.5]
    majorite_gagne = [r for r in avec_majorite
                      if (r["rouge_debut"] > 0.5) == (r["gagnante"] == ROUGE)]
    return {
        "parties": len(resultats),
        "converge_pct": 100 * len(converges) / len(resultats),
        "tours_moyen": statistics.mean(tours) if tours else None,
        "tours_median": statistics.median(tours) if tours else None,
        "tours_max": max(tours) if tours else None,
        "rouge_gagne_pct": 100 * len(rouges) / len(converges) if converges else None,
        "majorite_initiale_gagne_pct": (100 * len(majorite_gagne) / len(avec_majorite)
                                        if avec_majorite else None),
        "rouge_fin_moyen_pct": 100 * statistics.mean(r["rouge_fin"] for r in resultats),
    }
