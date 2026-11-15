# Journal de bord – Projet 2 (HAI716I)
 
## Protocole
- Tours par partie : 200
- Parties par paire : 5
- Graine aléatoire : 42 (pour que les résultats soient reproductibles )
- Self-play : activé.
Chaque stratégie joue aussi contre son double, comme dans le tournoi d’Axelrod. Ça représente le fait qu’un agent peut rencontrer des agents qui lui ressemblent.
Ce choix compte beaucoup : les stratégies gentilles gagnent beaucoup contre elles-mêmes (TIT-FOR-TAT contre TIT-FOR-TAT = 3 000 points, coopération totale), alors qu’ALL-D gagne peu contre lui-même (2 000 points, trahison totale).
J’ai testé les deux versions :avec self-play, TIT-FOR-TAT gagne ; sans self-play, ALL-D gagne. Le gagnant dépend donc d’un simple choix de protocole.
J’ai gardé le self-play pour la suite, parce que c’est le format d’Axelrod et que la sélection (étape 3) en a besoin : une stratégie qui se multiplie rencontre forcément ses copies.

## Stratégies
 
### ALL-D
- Règle : joue D à chaque tour, quoi que fasse l'adversaire.
- Origine : C'est le choix « rationnel » du dilemme
  joué une seule fois : trahir rapporte toujours plus, quoi que fasse l'autre.
- Devrait bien jouer contre :les stratégies imprévisibles comme RANDOM,
  car il gagne 5 points chaque fois que l'autre coopère.
- Devrait mal jouer contre : les stratégies qui réagissent à la trahison comme TIT-FOR-TAT, TESTER et JOSS ,ils se laissent tromper une seule fois puis trahissent aussi. Ainsi, ALL-D ne peut plus obtenir que 2 points par tour, contre 3 points lorsque les deux joueurs coopèrent.

### RANDOM
- Règle : à chaque tour, coopère avec une probabilité de 0,5 et trahit sinon,
  sans tenir compte de l'adversaire.
- Origine : Axelrod l'avait ajoutée à son tournoi de 1980
  comme point de comparaison , c'est comme une stratégie " sans intelligence " .
- Devrait bien jouer contre : Il peut gagner quelques points
  contre les stratégies qui coopèrent (il les trahit une fois sur deux).
- Devrait mal jouer contre : ALL-D, qui l'exploite chaque fois qu'il coopère
  (0 point pour RANDOM, 5 pour ALL-D)
  
### TIT-FOR-TAT
- Règle : coopère au premier tour, puis rejoue le dernier coup de l'adversaire.
- Origine : CM4 , la plus simple du tournoi , proposée par Anatol Rapoport, gagnante du tournoi d'Axelrod
- Devrait bien jouer contre : les stratégies gentilles et contre elle-même (3 points par tour).
- Devrait mal jouer contre :ALL-D (perd le premier tour) et JOSS (une trahison surprise lance un écho de vengeance)
### TESTER
- Règle : D au premier tour. Si l'adversaire riposte (joue D), TESTER joue TIT-FOR-TAT jusqu'à la fin ; sinon il répète C, C, D.
- Origine : CM4, stratégie soumise au tournoi d'Axelrod.
- Devrait bien jouer contre :les naïfs qui ne ripostent jamais : il les trahit un tour sur trois.
- Devrait mal jouer contre : Face à TIT-FOR-TAT, il trahit au premier tour. TFT riposte, puis TESTER, devenu TFT, imite cette riposte. Les deux stratégies entrent alors dans un cycle de représailles alternées (D, C, D, C…). Face à lui-même, les deux joueurs trahissent dès le premier tour, puis reproduisent indéfiniment la trahison de l'autre.
### JOSS
- Règle : TIT-FOR-TAT, mais remplace C par D une fois sur dix.
- Origine : CM4, soumise par Johann Joss au tournoi d'Axelrod.
- Devrait bien jouer contre : RANDOM et les stratégies qui ne ripostent pas.
- Devrait mal jouer contre : TFT, TESTER et lui-même : chaque trahison surprise déclenche une riposte, puis un cycle de vengeance qui fait baisser les deux scores.

## Étape 1 – Tournoi de base
 
### Commandes
```bash
python main.py --population base --seed 42
python main.py --population base --seed 42 --no-self-play
```
### Résultats 
## avec self-play 

![Étape 1 avec self-play](captures/base_1.png)

## sans self-play

![Étape 1 sans self-play](captures/base_2.png)


### Question : TIT-FOR-TAT gagne-t-il ?

**Oui avec self-play, mais de peu (12 026 contre 11 557 pour ALL-D).**

**Non sans self-play : ALL-D gagne.**

TFT ne remporte aucun duel direct, mais bénéficie d'un avantage important lorsqu'elle joue contre elle-même grâce à la coopération totale (3000 points). C'est cet avantage qui lui permet de gagner avec le self-play. Sans celui-ci, ALL-D prend l'avantage grâce à ses bons résultats contre RANDOM (3527 points). Enfin, TESTER est pénalisé par sa première trahison, qui déclenche un cycle de représailles et réduit son score.


**Pourquoi c'est différent du résultat de 1980 :**
1. **La population est trop petite et peu coopérative.** Il n'y a ici que 5 stratégies, et TFT est la seule
   « gentille » (qui ne trahit jamais la première). Elle n'a presque personne avec qui coopérer.
   Dans le tournoi d'Axelrod, il y avait beaucoup plus de programmes, et beaucoup étaient gentils
2. **Le protocole compte.** Le simple fait d'inclure ou non le self-play change le gagnant.
   Le résultat d'un tournoi dépend autant des règles du tournoi que des stratégies.

## Impasses 
1. **Première version de TESTER différente du cours.** Ma première version suivait une autre
   définition (TESTER s'excusait avant de passer en TFT, et trahissait un tour sur deux contre
   un naïf). Après comparaison avec la diapositive du CM4, je l'ai corrigée. Le classement a changé :
   avec self-play, TESTER était 1er et TFT 2e ; après correction, TFT est 1er et TESTER 3e.
   Un petit détail dans la règle d'une seule stratégie suffit à changer le gagnant.
   L'ancienne version est visible dans l'historique git.
2. **GENEROUS-TFT remplacée par TF2T** à l'étape 2, car elle est présentée dans le CM4
   et le sujet demande des stratégies absentes du cours.