![3n2am3hn](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/e2b9d704-cbde-459e-beb2-fd4a50137be7)

# HACKEMON -- WRITE UP

Bonjour à tous, dans ce document je vais vous proposer une solution au
challenge « Hackemon » issu de la phase de qualification du Hackday 2024

Pour commencer, on nous donne dans l'énoncé la commande unix permettant
de nous connecter au challenge à savoir : *nc* *challenges.hackday.fr*
*50392*

![uxgw1lhw](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/967d8e50-373b-40fb-8dc6-047a540d9af5)

Il nous suffit simplement pour l'instant de
suivre à la lettre ce qu'on nous demande, à savoir entrer notre adresse
mail.

![dwcklf3q](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/c43dd7e2-b655-4fe9-898c-831faf97fcfc)

![ifwacm2r](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/e6c57756-78f2-4928-afc3-53021bed36dc)


En vérifiant notre boîte mail, nous notons un nouveau message

Encore ici, il nous suffit de suivre ce qui nous est demandé :

Nous devons entrer dans l'ordre d'affichage dans l'email le nom japonais
de chacuns des pokémons représenté par les 5 cartes en pièces jointes.

L'ordre est le suivant :

> Pidgey -- Squirtle -- Bulbasaur -- Charmander -- Vulpix

Ce qui nous donne avec quelques recherches rapides sur internet :

> Poppo -- Zenigame -- Fushigidane -- Hitokage - Rokon

![d5qotthk](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/3a13394f-26ec-4b37-b09c-6ccc13b262f7)

En entrant chacun des 5 pokémons dans le bon ordre et en japonais, un
grand qr code s'affiche dans le terminal.

Si nous le scannons, nous sommes immédiatement redirigé vers un compte
instagram.

![33asryn0](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/f6226021-fd20-4b79-ad9c-e1e7b090d754)

![eveepi2j](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/cd794343-2415-46ed-955e-77a5d269ea96)

Nous tombons en effet sur un compte
*pikhackchuoff.* Cliquons sur la publication :

Regardons le commentaire posté
![33vqyuv0](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/7c2c433e-28db-4fdf-8b7e-60d9ae027008)

![s325mr22](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/09d1085a-4228-426a-8eb5-908afab22402)

On nous dit que celle ci n'est pas mal non plus en parlant certainement
d'une autre carte. Si nous allons sur le lien donné, nous tombons
effectivement sur une nouvelle carte :

Téléchargeons cette nouvelle carte...

(Un clique droit et « enregistrer sous » suffit)

On nous indique dans le cadre de la compétition que c'est un challenge
de stéganographie, tentons de voir si quelque chose ne se cache pas
derrière cette image.

De très nombreux outils peuvent être utilisés, ici j'utiliserai
*stegcracker* qui s'utilise très simplement.

![2qkcjpbw](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/46d64fe1-3c18-4e97-be88-373c0847a7e7)

La carte que nous avons téléchargé est dans le fichier pokeCard.jpg La
syntaxe de *stegcracker* est la suivante :

> *stegcracker* *\[attackedFile\]* *\[wordlist\]*

J'utilise ici la wordlist rockyou.txt, et en quelques secondes le mot de
passe *pikachu* est trouvé.

Notons que beaucoup d'autres bonnes wordlists aurait pu faire l'affaire
« pikachu » étant un mot assez courant et facilement retrouvable.

![ojbtmjap](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/c437d3dc-a469-43c6-aa47-0f71d9da4c86)

On nous indique de plus que le contenu
dissimulé derrière la carte a été écrit dans le fichier
*pokeCard.jpg.out*

![3n5pz3wn](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/ca1b2a68-d427-4a24-9dfb-102ab8ac18e9)

Affichons son contenu :

Nous remarquons un grand pikachu en ascii art avec en dessous ce qui
pourrait s'apparenter à une retranscription de la parole d'un pikachu.

Notre but est alors de traduire ce texte.

Après quelques recherches sur internet, nous tombons sur un langage
appelé le pikalang étant une version un peu stylisée du brainfuck.

![xknfkwml](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/a55dbfb5-6df4-41fd-8286-d1933f2db41b)

Nous trouvons très facilement un decodeur pikalang en ligne :

En exécutant, nous obtenons finalement, cette chaine de caractère :

> *The* *flag* *is* *HACKDAY{reverse_the_name_of_the_Pokemon_above}*

Rappelons que le pokémon au dessus était un pikachu, cloturant alors le
challenge avec le flag :

> ***HACKDAY{uhcakip}***
>
> *Auteur* *:* *YAM*
