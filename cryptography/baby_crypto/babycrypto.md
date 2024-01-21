# Baby Crypto
Nous avions un fichier en base64 (pour la portabilité).
Nous savons que son auteur sait compter et xorer, ce qui nous permet d'essayer diverses combinaisons dans cyberchef ou avec un petit script python:

- base64decode + xor '0123456789'
- base64decode + xor '1234567890'
- base64decode + xor '0123456789abcdef'
- base64decode + xor '123456789abcdef0'
Pour finir par comprendre qu'il faut compter en hexa:
- base64decode + xor '\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a...\xfe\xff'
Au final, le drapeau était formé par l'adresse mail trouvée dans le texte:
```
HACKDAY{C2endpoint@requiemC2.thm.htb.rm.fr}
```
