# Projet 2 (partie 1) – Tournoi d'Axelrod modifié (HAI716I)

Python 3. Seule dépendance optionnelle : `matplotlib` (graphique de la sélection).
```bash
pip install matplotlib
```

## Fichiers
- `moteur.py` : moteur (partie, tournoi, bruit, horizon inconnu, sélection)
- `strategies.py` : les stratégies et les populations (`base`, `etendue`)
- `main.py` : lance un tournoi, affiche le classement, écrit les CSV/PNG dans `results/`
- `test_ipd.py` : tests unitaires
- `journal.md` : journal de bord
- `captures/` : captures d'écran du journal

## Commandes

Tests :
```bash
python -m unittest -v
```

### Étape 1 – tournoi de base (5 stratégies du cours, 5 parties de 200 tours)
```bash
python main.py --population base --seed 42
python main.py --population base --seed 42 --no-self-play
```

### Étape 2 – population élargie (+ PAVLOV, TF2T)
```bash
python main.py --population etendue --seed 42
```

### Étape 3 – modifications du tournoi
Bruit (5 % des coups inversés) :
```bash
python main.py --population etendue --seed 42 --noise 0.05
```
Horizon inconnu (continue avec probabilité w = 0.99, soit 100 tours en moyenne) :
```bash
python main.py --population etendue --seed 42 --w 0.99
```
Sélection sur 100 générations (sans puis avec bruit) :
```bash
python main.py --population etendue --seed 42 --evolution 100
python main.py --population etendue --seed 42 --noise 0.05 --evolution 100
python main.py --population etendue --seed 42 --noise 0.05 --evolution 1000
```

## Options
`--seed`, `--rounds`, `--repeats`, `--population`, `--no-self-play`,
`--noise P`, `--w W`, `--evolution N`, `--out DOSSIER`.
Même graine => mêmes résultats.