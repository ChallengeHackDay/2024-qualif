# Hackday 2024: Can't you read that???

## Challenge information

**Category**: Forensic

**Description**: This challenge is about the de obfuscation of a file, to retrieve information about a potential attack.

## Solution

**Step 1: Initial analysis**

After the analysis of the nginx logs, we found that the attacker installed a webshell on the server.
The webshell is a PHP file, that allows the attacker to execute commands on the server.

With the logs, we managed to get the command executed by the attacker:
`python3+-c+"import zlib ; import base64 ; exec(zlib.decompress(base64.b64decode(%27eJytel2v5Lhx.........Zo2qer8L/R+TOcxN+mxNKjrr8AKKzZNg==%27)))"`

After replacing the `+` by a space, and the `%27` by a `'`, we can see that the command is a Python command, that imports the `zlib` and `base64` modules, and executes a command.

After decoding the string using CyberChef, we retrieve a complete script, that is obfuscated.

**Step 2: De-obfuscation**

To de-obfuscate the Python script, we can rename the variables to have a better understanding of the script.

We found a lot of dead code, that is not used by the script, and that is here to confuse the analyst.

After de-obfuscating the script, we can see that the script is a ransomware, that sends files to the attacker server, and encrypts them on the server.
We can also get the information needed to construct the flag.

### Flag

We can now construct the flag, with the information we found:
- Encryption IV: `bM8ftekoUEWCTbP5`
- Encryption key: `vLuUbS2o4i6Pr8jX`
- Attacker IP address: `13.98.138.213`
- Attacker port: `20304`
- Destination path: `/srv/www/dump/`
- Source path: `/home/`
- Encryption extension: `.enc`
- Flag structure: `HACKDAY{encryption_iv:encryption_key:attacker_ip:attacker_port:destination_path:source_path:encryption_extension}`

The flag is:
`HACKDAY{bM8ftekoUEWCTbP5:vLuUbS2o4i6Pr8jX:13.98.138.213:20304:/srv/www/dump/:/home/:.enc}`

## Creator

* Name: [Louis GAMBART](https://linkedin.com/in/louis-gambart)

## References

* [CyberChef](https://gchq.github.io/CyberChef/)
* [zlib documentation](https://docs.python.org/3/library/zlib.html)
* [base64 documentation](https://docs.python.org/3/library/base64.html)
