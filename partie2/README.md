# Projet 2 (partie 2) – Sujet B : le jeu du tee-shirt

Python 3. Dépendance optionnelle : `matplotlib` (graphiques `--courbes`).

## Fichiers
- `agent.py` : un agent (couleur, mémoire, gains)
- `regles.py` : les règles de mise à jour (MAJORITE, HCR, IMITATION, IMITATION_PROBA, WSLS, SEUIL)
- `jeu.py` : population, formation des paires (au hasard ou par voisinage), un tour, une partie
- `experiences.py` : une partie par graine, puis le résumé des mesures
- `main.py` : lance les expériences, affiche le tableau, écrit un CSV (et un graphique) dans `resultats/`
- `test_jeu.py` : tests unitaires
- `journal.md` : journal de bord de la partie 2

## Tests
```bash
python -m unittest -v
```

## Paramètres par défaut
N = 100 agents, mémoire m = 10, 1 000 tours maximum, 200 graines (0 à 199).
Les mêmes graines sont utilisées pour toutes les règles.

