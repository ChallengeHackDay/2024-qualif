
Pour ce challenge l'objectif est simple, déchiffrer le fichier ciphered flag dans la home d'un voisin.

on se connecte avec les creds découvert dans Baby Reverse Engineering:

```shell
$ ssh MemeMaster@challenges.hackday.fr -p 50391
MemeMaster@challenges.hackday.fr\'s password: Rubb3rDucky4Dock3r
Linux 74ceeb4dc66f 6.2.0-39-generic #40-Ubuntu SMP PREEMPT_DYNAMIC Tue Nov 14 14:18:00 UTC 2023 x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Mon Jan 22 19:16:23 2024 from 82.66.131.140
MemeMaster@74ceeb4dc66f:~$
```

observons les home voisine:

```shell
MemeMaster@74ceeb4dc66f:~$ ls ../*
../BootMaster:
cipheredflag  creds.txt

../BruteNinja:
creds.txt

../MemeMaster:
creds.txt
ls: cannot open directory '../Miro': Permission denied
```

Nous découvrons le cipheredflag mais celui ci est incompréhensible. Dans un challenge de forensic il peu être bon d'explorer les logs de la machine.

```shell
MemeMaster@74ceeb4dc66f:~$ ls /var/log
README  apt  btmp  docker-build.log  dpkg.log  faillog  journal  lastlog  private  runit  wtmp
```

le fichier docker-build.log est suspect. Son nom semble indiquer que les log ayant servi a un build docker y son inscris ces information son précieuse.

le fichier semble illisible je vais donc utiliser base 64 pour le rendre plus lisible

```shell
MemeMaster@74ceeb4dc66f:~$ base64 /var/log/docker-build.log
U2VuZGluZyBidWlsZCBjb250ZXh0IHRvIERvY2tlciBkYWVtb24gIDEwLjc1a0INDVN0ZXAgMS8x
...
```

ce fichier nous donne donc:

```shell
Sending build context to Docker daemon  10.75kB

Step 1/17 : FROM debian:latest
 ---> 2a033a8c6371
Step 2/17 : RUN useradd -ms /bin/bash MemeMaster
 ---> Running in abf97e0da1a4
Removing intermediate container abf97e0da1a4
 ---> 9d4b326d2ede
Step 3/17 : RUN echo 'MemeMaster:Rubb3rDucky4Dock3r' | chpasswd
 ---> Running in ff368b9d749c
Removing intermediate container ff368b9d749c
 ---> 21c7b5aff435
Step 4/17 : RUN chown -R root:user /home/MemeMaster && chmod 750 /home/MemeMaster
 ---> Running in f1656bceec92
Removing intermediate container f1656bceec92
 ---> 6d4f96553238
Step 5/17 : WORKDIR /home/MemeMaster
 ---> Running in 96566c2e7957
Removing intermediate container 96566c2e7957
 ---> 82a2099dcb5c
Step 6/17 : COPY "affinecipher.py" ./
 ---> d46feb8f3f9c
Step 7/17 : COPY "xorwithkey.py" ./
 ---> 4c7180351613
Step 8/17 : COPY "base64this.py" ./
 ---> 0995b04dd237
Step 9/17 : COPY "clearflag.txt" ./
 ---> b1450c2d0558
Step 10/17 : RUN apt-get update && apt-get install -y python3
 ---> Running in cada44bad601
Get:1 http://deb.debian.org/debian bookworm InRelease [151 kB]
Get:2 http://deb.debian.org/debian bookworm-updates InRelease [52.1 kB]
Get:3 http://deb.debian.org/debian-security bookworm-security InRelease [48.0 kB]
Get:4 http://deb.debian.org/debian bookworm/main amd64 Packages [8787 kB]
Get:5 http://deb.debian.org/debian bookworm-updates/main amd64 Packages [12.7 kB]
Get:6 http://deb.debian.org/debian-security bookworm-security/main amd64 Packages [134 kB]
Fetched 9185 kB in 3s (3267 kB/s)
Reading package lists...
Reading package lists...
Building dependency tree...
Reading state information...
The following additional packages will be installed:
  ca-certificates krb5-locales libexpat1 libgpm2 libgssapi-krb5-2 libk5crypto3
  libkeyutils1 libkrb5-3 libkrb5support0 libncursesw6 libnsl2
  libpython3-stdlib libpython3.11-minimal libpython3.11-stdlib libreadline8
  libsqlite3-0 libssl3 libtirpc-common libtirpc3 media-types openssl
  python3-minimal python3.11 python3.11-minimal readline-common
Suggested packages:
  gpm krb5-doc krb5-user python3-doc python3-tk python3-venv python3.11-venv
  python3.11-doc binutils binfmt-support readline-doc
The following NEW packages will be installed:
  ca-certificates krb5-locales libexpat1 libgpm2 libgssapi-krb5-2 libk5crypto3
  libkeyutils1 libkrb5-3 libkrb5support0 libncursesw6 libnsl2
  libpython3-stdlib libpython3.11-minimal libpython3.11-stdlib libreadline8
  libsqlite3-0 libssl3 libtirpc-common libtirpc3 media-types openssl python3
  python3-minimal python3.11 python3.11-minimal readline-common
0 upgraded, 26 newly installed, 0 to remove and 0 not upgraded.
Need to get 11.0 MB of archives.
After this operation, 36.5 MB of additional disk space will be used.
Get:1 http://deb.debian.org/debian bookworm/main amd64 libssl3 amd64 3.0.11-1~deb12u2 [2019 kB]
Get:2 http://deb.debian.org/debian bookworm/main amd64 libpython3.11-minimal amd64 3.11.2-6 [813 kB]
Get:3 http://deb.debian.org/debian bookworm/main amd64 libexpat1 amd64 2.5.0-1 [99.3 kB]
Get:4 http://deb.debian.org/debian bookworm/main amd64 python3.11-minimal amd64 3.11.2-6 [2064 kB]
Get:5 http://deb.debian.org/debian bookworm/main amd64 python3-minimal amd64 3.11.2-1+b1 [26.3 kB]
Get:6 http://deb.debian.org/debian bookworm/main amd64 media-types all 10.0.0 [26.1 kB]
Get:7 http://deb.debian.org/debian bookworm/main amd64 libncursesw6 amd64 6.4-4 [134 kB]
Get:8 http://deb.debian.org/debian bookworm/main amd64 libkrb5support0 amd64 1.20.1-2+deb12u1 [32.4 kB]
Get:9 http://deb.debian.org/debian bookworm/main amd64 libk5crypto3 amd64 1.20.1-2+deb12u1 [78.9 kB]
Get:10 http://deb.debian.org/debian bookworm/main amd64 libkeyutils1 amd64 1.6.3-2 [8808 B]
Get:11 http://deb.debian.org/debian bookworm/main amd64 libkrb5-3 amd64 1.20.1-2+deb12u1 [332 kB]
Get:12 http://deb.debian.org/debian bookworm/main amd64 libgssapi-krb5-2 amd64 1.20.1-2+deb12u1 [134 kB]
Get:13 http://deb.debian.org/debian bookworm/main amd64 libtirpc-common all 1.3.3+ds-1 [14.0 kB]
Get:14 http://deb.debian.org/debian bookworm/main amd64 libtirpc3 amd64 1.3.3+ds-1 [85.2 kB]
Get:15 http://deb.debian.org/debian bookworm/main amd64 libnsl2 amd64 1.3.0-2 [39.5 kB]
Get:16 http://deb.debian.org/debian bookworm/main amd64 readline-common all 8.2-1.3 [69.0 kB]
Get:17 http://deb.debian.org/debian bookworm/main amd64 libreadline8 amd64 8.2-1.3 [166 kB]
Get:18 http://deb.debian.org/debian bookworm/main amd64 libsqlite3-0 amd64 3.40.1-2 [837 kB]
Get:19 http://deb.debian.org/debian bookworm/main amd64 libpython3.11-stdlib amd64 3.11.2-6 [1796 kB]
Get:20 http://deb.debian.org/debian bookworm/main amd64 python3.11 amd64 3.11.2-6 [572 kB]
Get:21 http://deb.debian.org/debian bookworm/main amd64 libpython3-stdlib amd64 3.11.2-1+b1 [9312 B]
Get:22 http://deb.debian.org/debian bookworm/main amd64 python3 amd64 3.11.2-1+b1 [26.3 kB]
Get:23 http://deb.debian.org/debian bookworm/main amd64 openssl amd64 3.0.11-1~deb12u2 [1419 kB]
Get:24 http://deb.debian.org/debian bookworm/main amd64 ca-certificates all 20230311 [153 kB]
Get:25 http://deb.debian.org/debian bookworm/main amd64 krb5-locales all 1.20.1-2+deb12u1 [62.7 kB]
Get:26 http://deb.debian.org/debian bookworm/main amd64 libgpm2 amd64 1.20.7-10+b1 [14.2 kB]
[91mdebconf: delaying package configuration, since apt-utils is not installed
[0mFetched 11.0 MB in 1s (11.0 MB/s)
Selecting previously unselected package libssl3:amd64.
(Reading database ... 
(Reading database ... 5%
(Reading database ... 10%
(Reading database ... 15%
(Reading database ... 20%
(Reading database ... 25%
(Reading database ... 30%
(Reading database ... 35%
(Reading database ... 40%
(Reading database ... 45%
(Reading database ... 50%
(Reading database ... 55%
(Reading database ... 60%
(Reading database ... 65%
(Reading database ... 70%
(Reading database ... 75%
(Reading database ... 80%
(Reading database ... 85%
(Reading database ... 90%
(Reading database ... 95%
(Reading database ... 100%
(Reading database ... 6098 files and directories currently installed.)
Preparing to unpack .../libssl3_3.0.11-1~deb12u2_amd64.deb ...
Unpacking libssl3:amd64 (3.0.11-1~deb12u2) ...
Selecting previously unselected package libpython3.11-minimal:amd64.
Preparing to unpack .../libpython3.11-minimal_3.11.2-6_amd64.deb ...
Unpacking libpython3.11-minimal:amd64 (3.11.2-6) ...
Selecting previously unselected package libexpat1:amd64.
Preparing to unpack .../libexpat1_2.5.0-1_amd64.deb ...
Unpacking libexpat1:amd64 (2.5.0-1) ...
Selecting previously unselected package python3.11-minimal.
Preparing to unpack .../python3.11-minimal_3.11.2-6_amd64.deb ...
Unpacking python3.11-minimal (3.11.2-6) ...
Setting up libssl3:amd64 (3.0.11-1~deb12u2) ...
Setting up libpython3.11-minimal:amd64 (3.11.2-6) ...
Setting up libexpat1:amd64 (2.5.0-1) ...
Setting up python3.11-minimal (3.11.2-6) ...
Selecting previously unselected package python3-minimal.
(Reading database ... 
(Reading database ... 5%
(Reading database ... 10%
(Reading database ... 15%
(Reading database ... 20%
(Reading database ... 25%
(Reading database ... 30%
(Reading database ... 35%
(Reading database ... 40%
(Reading database ... 45%
(Reading database ... 50%
(Reading database ... 55%
(Reading database ... 60%
(Reading database ... 65%
(Reading database ... 70%
(Reading database ... 75%
(Reading database ... 80%
(Reading database ... 85%
(Reading database ... 90%
(Reading database ... 95%
(Reading database ... 100%
(Reading database ... 6426 files and directories currently installed.)
Preparing to unpack .../00-python3-minimal_3.11.2-1+b1_amd64.deb ...
Unpacking python3-minimal (3.11.2-1+b1) ...
Selecting previously unselected package media-types.
Preparing to unpack .../01-media-types_10.0.0_all.deb ...
Unpacking media-types (10.0.0) ...
Selecting previously unselected package libncursesw6:amd64.
Preparing to unpack .../02-libncursesw6_6.4-4_amd64.deb ...
Unpacking libncursesw6:amd64 (6.4-4) ...
Selecting previously unselected package libkrb5support0:amd64.
Preparing to unpack .../03-libkrb5support0_1.20.1-2+deb12u1_amd64.deb ...
Unpacking libkrb5support0:amd64 (1.20.1-2+deb12u1) ...
Selecting previously unselected package libk5crypto3:amd64.
Preparing to unpack .../04-libk5crypto3_1.20.1-2+deb12u1_amd64.deb ...
Unpacking libk5crypto3:amd64 (1.20.1-2+deb12u1) ...
Selecting previously unselected package libkeyutils1:amd64.
Preparing to unpack .../05-libkeyutils1_1.6.3-2_amd64.deb ...
Unpacking libkeyutils1:amd64 (1.6.3-2) ...
Selecting previously unselected package libkrb5-3:amd64.
Preparing to unpack .../06-libkrb5-3_1.20.1-2+deb12u1_amd64.deb ...
Unpacking libkrb5-3:amd64 (1.20.1-2+deb12u1) ...
Selecting previously unselected package libgssapi-krb5-2:amd64.
Preparing to unpack .../07-libgssapi-krb5-2_1.20.1-2+deb12u1_amd64.deb ...
Unpacking libgssapi-krb5-2:amd64 (1.20.1-2+deb12u1) ...
Selecting previously unselected package libtirpc-common.
Preparing to unpack .../08-libtirpc-common_1.3.3+ds-1_all.deb ...
Unpacking libtirpc-common (1.3.3+ds-1) ...
Selecting previously unselected package libtirpc3:amd64.
Preparing to unpack .../09-libtirpc3_1.3.3+ds-1_amd64.deb ...
Unpacking libtirpc3:amd64 (1.3.3+ds-1) ...
Selecting previously unselected package libnsl2:amd64.
Preparing to unpack .../10-libnsl2_1.3.0-2_amd64.deb ...
Unpacking libnsl2:amd64 (1.3.0-2) ...
Selecting previously unselected package readline-common.
Preparing to unpack .../11-readline-common_8.2-1.3_all.deb ...
Unpacking readline-common (8.2-1.3) ...
Selecting previously unselected package libreadline8:amd64.
Preparing to unpack .../12-libreadline8_8.2-1.3_amd64.deb ...
Unpacking libreadline8:amd64 (8.2-1.3) ...
Selecting previously unselected package libsqlite3-0:amd64.
Preparing to unpack .../13-libsqlite3-0_3.40.1-2_amd64.deb ...
Unpacking libsqlite3-0:amd64 (3.40.1-2) ...
Selecting previously unselected package libpython3.11-stdlib:amd64.
Preparing to unpack .../14-libpython3.11-stdlib_3.11.2-6_amd64.deb ...
Unpacking libpython3.11-stdlib:amd64 (3.11.2-6) ...
Selecting previously unselected package python3.11.
Preparing to unpack .../15-python3.11_3.11.2-6_amd64.deb ...
Unpacking python3.11 (3.11.2-6) ...
Selecting previously unselected package libpython3-stdlib:amd64.
Preparing to unpack .../16-libpython3-stdlib_3.11.2-1+b1_amd64.deb ...
Unpacking libpython3-stdlib:amd64 (3.11.2-1+b1) ...
Setting up python3-minimal (3.11.2-1+b1) ...
Selecting previously unselected package python3.
(Reading database ... 
(Reading database ... 5%
(Reading database ... 10%
(Reading database ... 15%
(Reading database ... 20%
(Reading database ... 25%
(Reading database ... 30%
(Reading database ... 35%
(Reading database ... 40%
(Reading database ... 45%
(Reading database ... 50%
(Reading database ... 55%
(Reading database ... 60%
(Reading database ... 65%
(Reading database ... 70%
(Reading database ... 75%
(Reading database ... 80%
(Reading database ... 85%
(Reading database ... 90%
(Reading database ... 95%
(Reading database ... 100%
(Reading database ... 6934 files and directories currently installed.)
Preparing to unpack .../python3_3.11.2-1+b1_amd64.deb ...
Unpacking python3 (3.11.2-1+b1) ...
Selecting previously unselected package openssl.
Preparing to unpack .../openssl_3.0.11-1~deb12u2_amd64.deb ...
Unpacking openssl (3.0.11-1~deb12u2) ...
Selecting previously unselected package ca-certificates.
Preparing to unpack .../ca-certificates_20230311_all.deb ...
Unpacking ca-certificates (20230311) ...
Selecting previously unselected package krb5-locales.
Preparing to unpack .../krb5-locales_1.20.1-2+deb12u1_all.deb ...
Unpacking krb5-locales (1.20.1-2+deb12u1) ...
Selecting previously unselected package libgpm2:amd64.
Preparing to unpack .../libgpm2_1.20.7-10+b1_amd64.deb ...
Unpacking libgpm2:amd64 (1.20.7-10+b1) ...
Setting up media-types (10.0.0) ...
Setting up libkeyutils1:amd64 (1.6.3-2) ...
Setting up libgpm2:amd64 (1.20.7-10+b1) ...
Setting up libtirpc-common (1.3.3+ds-1) ...
Setting up libsqlite3-0:amd64 (3.40.1-2) ...
Setting up krb5-locales (1.20.1-2+deb12u1) ...
Setting up libkrb5support0:amd64 (1.20.1-2+deb12u1) ...
Setting up libncursesw6:amd64 (6.4-4) ...
Setting up libk5crypto3:amd64 (1.20.1-2+deb12u1) ...
Setting up libkrb5-3:amd64 (1.20.1-2+deb12u1) ...
Setting up openssl (3.0.11-1~deb12u2) ...
Setting up readline-common (8.2-1.3) ...
Setting up libreadline8:amd64 (8.2-1.3) ...
Setting up ca-certificates (20230311) ...
debconf: unable to initialize frontend: Dialog
debconf: (TERM is not set, so the dialog frontend is not usable.)
debconf: falling back to frontend: Readline
debconf: unable to initialize frontend: Readline
debconf: (Can't locate Term/ReadLine.pm in @INC (you may need to install the Term::ReadLine module) (@INC contains: /etc/perl /usr/local/lib/x86_64-linux-gnu/perl/5.36.0 /usr/local/share/perl/5.36.0 /usr/lib/x86_64-linux-gnu/perl5/5.36 /usr/share/perl5 /usr/lib/x86_64-linux-gnu/perl-base /usr/lib/x86_64-linux-gnu/perl/5.36 /usr/share/perl/5.36 /usr/local/lib/site_perl) at /usr/share/perl5/Debconf/FrontEnd/Readline.pm line 7.)
debconf: falling back to frontend: Teletype
Updating certificates in /etc/ssl/certs...
140 added, 0 removed; done.
Setting up libgssapi-krb5-2:amd64 (1.20.1-2+deb12u1) ...
Setting up libtirpc3:amd64 (1.3.3+ds-1) ...
Setting up libnsl2:amd64 (1.3.0-2) ...
Setting up libpython3.11-stdlib:amd64 (3.11.2-6) ...
Setting up libpython3-stdlib:amd64 (3.11.2-1+b1) ...
Setting up python3.11 (3.11.2-6) ...
Setting up python3 (3.11.2-1+b1) ...
running python rtupdate hooks for python3.11...
running python post-rtupdate hooks for python3.11...
Processing triggers for libc-bin (2.36-9+deb12u3) ...
Processing triggers for ca-certificates (20230311) ...
Updating certificates in /etc/ssl/certs...
0 added, 0 removed; done.
Running hooks in /etc/ca-certificates/update.d...
done.
Removing intermediate container cada44bad601
 ---> 10d0b91b2a5c
Step 11/17 : RUN "python3" "affinecipher.py" "clearflag.txt"
 ---> Running in ae3f947636db
Removing intermediate container ae3f947636db
 ---> fed9b9a84d51
Step 12/17 : RUN "python3" "xorwithkey.py" "clearflag.txt" "HACKDAY"
 ---> Running in f01dd4c4e5e3
Removing intermediate container f01dd4c4e5e3
 ---> 638d5a463650
Step 13/17 : RUN "python3" "base64this.py" "clearflag.txt"
 ---> Running in 50c0691102ad
Removing intermediate container 50c0691102ad
 ---> 11f892281b42
Step 14/17 : RUN mv clearflag.txt cipheredflag
 ---> Running in c0aa56107988
Removing intermediate container c0aa56107988
 ---> d8ccf043b854
Step 15/17 : RUN rm *.py
 ---> Running in 7b0f33385156
Removing intermediate container 7b0f33385156
 ---> 6926e3323022
Step 16/17 : USER MemeMaster
 ---> Running in 20994f579a64
Removing intermediate container 20994f579a64
 ---> 53846d5663a3
Step 17/17 : CMD [ "/bin/bash" ]
 ---> Running in 4339991066a0
Removing intermediate container 4339991066a0
 ---> 5f268e142dc7
Successfully built 5f268e142dc7
Successfully tagged logmein_image:latest
```

on peu voir grâce a l'étape 11 à 13 les modifications qui ont été apporter au fichier il suffit de les effectuer dans l'ordre inverse.

en python on peu coder les fonctions qui vont respectivement base64 decode , xor puis enfin casser le chiffrement affine:

```python
from base64 import b64decode

def xor(a:bytes):
	b = b"HACKDAY"
	c = [a[i%len(a)]^b[i%len(b)] for i in range(len(a))] 
	return bytes(c) 

def guessaffine(c:bytes):
	p = b"HACKDAY{"
	C0, C1 = c[0]-65,c[1]-65 
	P0, P1 = p[0]-65,p[1]-65 
	a = (C0-C1 % 26)*pow((P0-P1 % 26), -1, 26) % 26
	print(f"---GUESSING a is {a}---") # Good is 7
	b = C1-a*P1
	print(f"---GUESSING b is {b}---") # Good is 16
	return affinedecode(c, a, b)

def affinedecode(c:bytes, a:int, b:int): 
	p = []
	for letter in c:
		if 30 <= letter and letter <= 39: 
			p.append((letter-30-b % 26) * pow(a,-1,26) %26 + 30)
		elif 65 <= letter and letter <= 90:
			p.append((letter-65-b % 26) * pow(a,-1,26) %26 + 65)
		else: 
			p.append(letter)
	return bytes(p)

cipheredflag = "BhAGAggQ..."
print(guessaffine(xor(b64decode(cipher))).decode())
```

cela nous donnera:

```
INTERCEPTED COMMUNICATION REPORTS:

I. LOCATION OF THE TARGET
USING NEW OSINT METHODS, I WAS ABLE TO EFFICIENTLY LOCATE THE HOME OF THE HEAD OF SECURITY, WHICH WAS LOCATED AT 4 QUAI DES ORFÈVRES IN PARIS. 


II. SOCIAL ENGINEERING
USING AN INNOVATIVE METHOD OF SOCIAL ENGINEERING, AND NOTICING THAT HE HAD CAST-IRON WATER RADIATORS, I ENTERED HIS HOME TO EMPTY THE RADIATORS. I TOOK THE OPPORTUNITY TO PLACE MICROPHONES IN VARIOUS PARTS OF THE HOUSE. I ALSO INSTALLED A REMOTELY CONTROLLABLE USB IMPLANT IN THE BACK OF THE FAMILY COMPUTER.

III. LOCAL ADMIN
THIS COMPUTER WAS MORE ROBUST THAN EXPECTED... THE MACHINE WAS UP TO DATE AND THE PRIVILEGES WERE WELL SEGMENTED. HOWEVER, A DEEP ENUMERATION OF THE BACKUP SYSTEM ALLOWED ME TO FIND A TXT FILE CONTAINING THE ADMINISTRATOR'S CREDENTIALS IN THE OLDEST STILL VALID BACKUP. A WEEK LATER AND THE FILE WOULD HAVE BEEN DELETED AUTOMATICALLY.

IV. OBJECTIVE REACHED
WE RECOVERED THE RESOURCES WE NEEDED TO MAKE OUR MOVE. THESE RESOURCES ARE ON OUR USUAL GOOGLE DRIVE. MORE INSTRUCTIONS TO FOLLOW.

JOHN B.

HACKDAY{CH3CK_Y0UR_L0GS}
```
