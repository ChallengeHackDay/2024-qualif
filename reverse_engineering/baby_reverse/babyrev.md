# Baby Reverse
Here is the [link](https://cloud.binary.ninja/bn/2fa79432-96e3-40ec-a19a-55b6f1e47c40) to my binary ninja session (requires an account to have access to).

This challenge was about reversing an unusual keypass.exe. Don't let the name fool you, it is NOT a clone nor a copy of the real [keepass](https://keepass.info/) tool .

Only a static analysis of this tool was required to solve. By putting it in binary ninja, we could go to the main function and see :

- __builtin_strncpy(&key, "Memes4EveeeeeeeR", 0x10)
- __builtin_memcpy(&encrpyted_password_buffer, "\x95\x00\x00\x00\x85\x00\x00\x00\x77\x00\x00\x00\x06\x00\x00\x00\xb7\x00\x00\x00\xa7\x00\x00\x00\x24\x00\x00\x00\x7b\x00\x00\x00\x92\x00\x00\x00\xa8\x00\x00\x00\xc9\x00\x00\x00\x29\x00\x00\x00\x57\x00\x00\x00\x76\x00\x00\x00\xd4\x00\x00\x00\xd6\x00\x00\x00\xb1\x00\x00\x00\x14\x00\x00\x00\x6a\x00\x00\x00\xdb\x00\x00\x00\x98\x00\x00\x00\xb0\x00\x00\x00\x32\x00\x00\x00\x3c\x00\x00\x00\x8a\x00\x00\x00\x5f\x00\x00\x00\x08\x00\x00\x00\x22\x00\x00\x00\xac\x00\x00\x00\x5d\x00\x00\x00\xe0\x00\x00\x00\xa5\x00\x00\x00\xa9\x00\x00\x00\x24\x00\x00\x00\x24\x00\x00\x00\x3c\x00\x00\x00", 0x90) int32_t  var_98 = 0x7b char  userinput char*  rax = fgets(&userinput, 0x40, stdin) int32_t  rax_8 if (rax != 0)
- rc4_init(&key, 0x10, &rc4_object)

Clearly, the binary has the password stored as a RC4 bytestring. We have the key next to it, which is good. Time to whip out cyberchef.
Put the big hex string in the ingredients and for the recipe:
Just choose:
- **From hex**
- **Remove null bytes**
- **RC4** and put the key inside the box

You have cooked your flag, which can also get vaildated through the binary:

```
HACKDAY{MemeMaster:Rubb3rDucky4Dock3r}
```
