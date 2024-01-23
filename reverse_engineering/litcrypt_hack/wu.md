# Litcrypt
This chall is based on the use of litteral encryption in rust lang to hide some important informations. A quick search on rust litcrypt with the chall title give us a rust library : https://github.com/anvie/litcrypt.rs. Keep it in mind for later!

## First steps
First, when we launch the binary, we are asked to type a password. As the guess is false, we got a "Wrong password" printed. 

![image](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/db68f9f9-6423-4e1d-b3c5-8cabe9cf2a6b)


A quick **strings** on the binary with a grep has no match with anything that looks like a flag. sad. 

Let begin the reverse. 

![image](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/ed8f6631-ea8b-4228-b615-c9667310a348)


## Decompile 
I personnaly use ida, but I think any other should be fine. first, lets dissassemble the binary and take a look. The first point is to find where the string Wrong password is called, and look around, we shoud have a comparaison around this point. 

![image](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/f09a5c01-e2dd-4903-867c-924eebf66bf1)


Here, we can see a function called "admintool::licryptinternal::decryptbytes" with two parameters that seems to be random. But there is no ransomness here ! If we take a look at the rust library, we easly find that xor is used to encrypt the key with a static key : 'l33t'... If we take the smallest argument from the function call, and xor it with the static key, we find the key used for litteral encryption : 'HACKDAY'...

![image](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/f0ddcab0-2749-4a7f-8c41-4611f86b2f17)

It is fun, but useless for the challenge. The interessesting part is the first argument, which contains the flag. The string is basicly just xored with the second argument, and here we can find the flag to validate the challenge. 

![image](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/39024aa4-8395-4bc9-9103-3fb1481a7d7a)
