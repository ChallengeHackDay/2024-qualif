# Assurance Tourix

Ce challenge est un challenge principalement autour des APIs. Le serveur web sert
plusieurs APIs et un frontend minimal.

## Création d'un compte utilisateur

On arrive sur le front, pas d'interface pour se register, Dans la requête du login, 
on voit des appels à une api : `/apis/auth/v1/`

![login_request](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/a2da34c6-08d2-4094-9b7e-27cc24219100)

On sait que la configuration OpenAPI est exposée, on peut donc y accéder via l'url
suivate :
`/apis/auth/v1/openapi.json`.

![auth_openapi](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/7a9060c1-79b5-4b3f-ab23-a063300d9245)

> **Note :** les urls `/apis/auth/v1/openapi.yml` et `/apis/auth/v1/openapi.yaml`
> renvoient une 301 vers la bonne url du fichier OpenAPI : `/apis/auth/v1/openapi.json`.

On peut parser le fichier OpenAPI avec https://editor.swagger.io/.

![auth_swagger](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/f7d8aeff-4c1d-4b59-8839-b81a867a0d7d)

On retrouve donc un endoit permettant de s'enregistrer : `/apis/auth/v1/register`.

Nous nous enregistrons.

On peut donc par la suite se connecter (via l'interface ou via `/apis/auth/v1/login`).

L'API nous renvoie un token JWT.

## Attaque du JWT

Nous pouvons par la suite regarder le contenu du JWT (ex : https://jwt.io/)

On voit dans la payload du JWT un Array `roles` qui ne contient que la string
`"customer"`.

Etant donné que le token est chiffré avec un algorithme symétrique nous pouvons essayer
de le bruteforce en offline.

![bruteforce_jwt](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/f55a1a45-2afb-4fdb-be85-e935819fa4ff)

Le mot de passe est faible et est contenu dans rockyou.

Par la suite, nous pourrons ajouter le role `"admin"` et forge ce token avec le secret
retrouvé.

![add_admin_role](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/3d83d71f-2e1e-47ea-b327-1209a9e3c7ea)

## Accès à l'API d'administration

Si nous regardons dans le fichier OpenAPI de l'API d'authentification nous pouvons
retrouver l'endpoint `/apis/auth/v1/informations` qui nous permet d'énumérer les
APIs qui sont accessibles par l'utilisateur.

![available_api_paths](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/4b4cfa3b-8924-446a-b75c-9a450e24fe2d)

Avec le role `"admin"` l'utilisateur a désormais accès à l'API d'administration.

Nous pouvons énumérer les endpoints via le OpenAPI : 

![admin_openapi](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/948e08e5-316d-4ff3-bfc0-f1d8856afe4e)

![send_message](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/15932106-998c-4cc2-8fd1-1b502d390ea7)

Il suffira à l'agent de répondre à un ticket afin de récupérer le flag : 

![get_flag](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/f1f613ad-b2e1-4dcc-81ff-75093dcef327)
