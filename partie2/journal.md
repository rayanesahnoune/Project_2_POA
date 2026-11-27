## 0. Démarrage – vendredi 27/11, [heure]
- Sujet choisi : B, le jeu du tee-shirt. Je l'ai choisi parce qu'il ressemble à la sélection
  de la partie 1 (une population qui évolue), et que le résultat se voit bien sur des courbes.
- Ce que j'ai compris : 100 agents portent un tee-shirt rouge ou bleu. À chaque tour, ils se
  rencontrent deux par deux au hasard et gagnent 1 point s'ils ont la même couleur. Ensuite,
  chacun garde ou change sa couleur selon sa règle. On regarde si tout le monde finit de la
  même couleur.
- Lien avec les systèmes multi-agents : une convention apparaît sans chef et sans que personne
  ne voie toute la population.

## 1. Protocole

| Paramètre | Valeur | Pourquoi |
|---|---|---|
| Population N | 100 | nombre pair (tout le monde a un partenaire), assez grand pour une vraie population |
| Mémoire m | 10 | assez pour ne pas changer au moindre hasard, assez court pour réagir vite |
| Tours maximum | 1 000 | au-delà, on considère que la partie ne converge pas |
| Graines | 200 (0 à 199) | assez de parties pour calculer des pourcentages fiables |
| Gain | 1 si même couleur, 0 sinon | règle du cours |
| Égalité | l'agent garde sa couleur | pour ne favoriser ni le rouge ni le bleu |
| Ordre dans un tour | tout le monde observe, puis tout le monde change | pour que l'ordre des agents ne change pas le résultat |
| Convergence | les 100 agents ont la même couleur | définition du sujet |

**Vérification à la main :** un agent BLEU a vu R, R, B dans sa mémoire. Avec HCR, porter
rouge lui aurait rapporté 2 points, porter bleu 1 point : il passe ROUGE.
Le test `test_hcr_change_si_autre_couleur_plus_vue` vérifie que le programme fait pareil.
