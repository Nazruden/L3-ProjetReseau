# L3 - Projet de Réseau (Semestre 5 parcours Licence Informatique)
Projet de Réseau du S5 parcours Licence informatique à l'Université de Bordeaux - collège sciences et technologies.

# Sujet
Mettre en réseau un jeu de morpion.

# Protocole de communication client <> serveur
|   Commande    |   Source    |   Arguments   |   Retour    |   Description   |
| ------------- | :----------:| ------------- | ----------- | --------------- |
| GETSTATE | Client | NULL | Grille actuelle | Récupération et mise à jour de la grille |
| GETSCORE | Client | NULL | Score actuel | Récupération et mise à jour du score. |
| CONNECT | Client | Serveur cible | Etat de la connexion | Effectuer une demande de connexion. |
| DISCONNECT | Client | NULL | Etat de la connexion | Effectuer une demande de déconnexion. |
| PLACE | Client | Case ciblée | Message d'état | Commande permettant de placer un jeton sur la case spécifiée. Retourne le message d'état post-traitement |

## Client :
### A coder
Gestion récupération de messages
Cmd "GETSTATE" : Le joueur doit pouvoir récupérer les données de la grille.
Cmd "GETSCORE" : Le joueur doit pouvoir récupérer le score.

On imagine ainsi que la gestion de la cohérence est faite par le serveur et garantie au travers des échanges.

### Actions que pourra effectuer le joueur :
Cmd "PLACE x" : Le joueur doit pouvoir effectuer des demandes de placement de jetons.
Cmd "CONNECT"
Cmd "DISCONNECT"

## Serveur :
### A coder
Le serveur doit pouvoir gérer les commandes des joueurs suivantes :
* PLACE
* GETSTATE
* GETSCORE
* CONNECT
* DISCONNECT


