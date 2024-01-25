The file is not readable as it stands because it contains a series of 0x00 at the beginning and end of the file. Deleting them produces a strange text file consisting of K, X, C and D.

![Pasted image 20240124022402](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/09cead03-3921-4e05-9955-99877b6eb3c4)

This character alphabet corresponds to a derivative of **deadfish** the [**deadfish x**](https://esolangs.org/wiki/Deadfish_x) an interpreter is available on [dcode](https://www.dcode.fr/deadfish-language) 

this gives us the following sequence of numbers :

**110 101 103 113 104 101 131 173 122 60 104 137 120 110 61 123 110 61 116 107 137 61 123 137 64 127 63 123 60 115 63 175**

[cyberchef](https://gchq.github.io/CyberChef) will find quickly the octal representation of the ASCII characters

HACKDAY{R0D_PH1SH1NG_1S_4W3S0M3}
