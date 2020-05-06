# AVALAM-PROJECT
Project Avalam
Règles du jeu:
http://www.oya.fr/?post/2014/12/09/73-avalam-est-a-oya

L'IA est basée sur le framework easyAI, voir:
https://github.com/Zulko/easyAI/blob/master/README.rst

L'IA utilise Negamax, une variante de l'algorithme Minimax avec élagage 'alpha/beta' afin d'optimiser la recherche.
https://en.wikipedia.org/wiki/Negamax

Pour évaluer l'état du jeu, Negamax utilise La fonction Avalam.scoring(). Celle ci calcule dans un premier temps le nombre de tours que possède chaque équipe (le score direct). Ensuite, elle cherche si cette tour pourrait encore se déplacer ou être prise par l'adversaire. Si non, c'est qu'elle est 'figée'. Elle ne bougera plus de la partie, donc le point qu'elle rapporte peut être considéré comme acquis. Ces tours valorisent le score du joueur qui la possède.

Pour jouer contre l'ia dans le terminal, appeler la fonction human_vs_ai(human_color=1).
Pour voir jouer l'ia contre random, appeler la fonction random_vs_ai(random_color=1).

Pour obtenir de l'ia un seul coup sans jouer toute la partie, appeler la fonction AI_runner(state=body). (body == état du jeu reçu part le serveur).



Lorsqu'on joue human_vs_ai():
'Player 1' a les pions '0' et 'Player 2' a les pions '1'    
Les tours sont représentées par un tuple de forme (pion dominant la tour, nbr de pions dans la tour)
Quand c'est au tour de Human_Player de jouer, le joueur peut rentrer dans la ligne de commande:
    - le mouvement à jouer, sous forme de 4 numéros 'ab cd' avec a=ligne 'from', b=colonne 'from', c=ligne 'to', d=colonne 'to'
    - 'show moves' pour montrer tous les coups possibles
    - 'move #nbr' pour jouer le coups numéro 'nbr' proposés par 'show moves'
    - 'quit' pour interrompre le jeu
