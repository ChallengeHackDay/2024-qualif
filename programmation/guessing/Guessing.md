
Pour cette épreuve, nous allons nous connecter à une instance qui nous envoie un message assez cryptique.

Rien de très compréhensible, mais en générant une dizaine de messages, on comprends que la taille du message ne change jamais et que certains caractères reviennent assez souvent.

Il suffit alors de faire une analyse statistique de chaque caractère pour comprendre que la valeur de chaque caractère, en ascii, est aléatoirement calculée. On lui fait, au hasard, +1, 0 ou -1.

Pour avoir la bonne lettre, il faut toujours prendre celle du milieu, et on retrouve le texte: (la réponse était 42)
```
< Hello stranger.
< Since you are so good at guessing, can you give me the number ?
> 42
< Great ! Access to the secret file has been granted HACKDAY{N0T_So_GUESSY_HUH??} :
```
En bonus, vous aviez un fichier en base64 qui contenait des informations relatives au lore.
