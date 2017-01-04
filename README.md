# L3 - Projet de Réseau (Semestre 5 parcours Licence Informatique)
Projet de Réseau du S5 parcours Licence informatique à l'Université de Bordeaux - collège sciences et technologies.

# Sujet
Mettre en réseau un jeu de morpion.

# Protocole de communication client <> serveur
|   Commande    |   Source    |   Arguments   |   Retour    |   Description   |
| ------------- | :----------:| ------------- | ----------- | --------------- |
| UPDATE | Client | NULL | Grille actuelle | Mise à jour de l'environnement de jeu auprès du joueur. |
| PLACE | Client | Case ciblée | Message d'état | Commande permettant de placer un jeton sur la case spécifiée. Retourne le message d'état post-traitement |
|
## Client :
Cmd "PLACE x" : Le joueur doit pouvoir effectuer des demandes de placement de jetons.
Cmd "UPDATE" : Le joueur doit pouvoir récupérer les données de la grille.
On imagine ainsi que la gestion de la cohérence est faite par le serveur et garantie au travers des échanges.

## Serveur :
Le serveur doit pouvoir gérer les commandes des joueurs :
* PLACE
* UPDATE
* CONNECT
* DISCONNECT

