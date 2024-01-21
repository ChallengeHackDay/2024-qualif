# Secret Password
Pas très compliqué. Après s'être connectés à l'instance, nous recevons une liste de caractères valides ainsi qu'une nombre de caractères. La machine va ensuite nous demander le mot de passe.
Lorsque nous envoyons un mot à la machine, elle nous réponds avec le nombre de lettres étant au bon endroit dans le mot de passe. Ma méthode de résolution à été:

- Récupérer la liste de caractères valides et la longueur du mot recherché
- Envoyer des lignes du même caractère
- Nous avons donc une liste des caractères valide
- Nous prenons la première lettre qui n'existe pas dans le mot et nous essayons toutes les positions pour une lettre valide.

Tout cela, trois fois!

Exemple:
```
> aaaaa
< 2 bons
> bbbbb
< 0 bons
> ccccc
< 1 bon
> ddddd
< 2 bons
Nous avons la liste: ["a", "c", "d"]
On essaye:
> abbbb
< 0 bon (pas bon emplacement de a)
> babbb
< 1 bon // on sait qu'il y a un a en deuxième position
etc...
```
Au bout de trois fois, on récupère du lore, avec le flag à la fin:

```
HACKDAY{Whispers_in_the_D4rk}
```
