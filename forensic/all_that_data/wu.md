# Hackday 2024: All that data???

## Challenge information

**Category**: Forensic

**Description**: This challenge is about the analysis of nginx logs to retrieve information about a potential attack.

## Solution

**Step 1: Initial analysis**

We are given two files: `access.log` and `error.log`.
The first contains the common log format of nginx, and the second contains the error log of nginx.

In the `error.log` file, nothing relevant is found.

**Step 2: Access log analysis**

In the `access.log` file, we can see that there are a lot of requests to different pages, using **GET**, that came from the same requester.

Here, we can say that the requester performed a scan of the website, like `dirb` or `gobuster` would do.
This is a directory-based attack to find hidden pages on a website.

![image](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/eb61199f-2213-4066-b0b2-47b85028268a)

Always in the `access.log` file, we can see that there are a lot of requests to the same page, using **POST**, that came from the same requester.

Here, we can say that the attacker performed a brute-force attack on the admin login page of the website.

![image](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/161af0fb-f505-4ef4-97de-3d06a6857881)

We can now see that the attacker managed to find the admin password, and logged in.

After that, we can see that the attacker install a plugin on the website.

![image](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/6b9e8b80-bb39-4197-9dba-b61cfd813c4c)

This plugin is webshell, that allows the attacker to execute commands on the server.

We see the command executed by the attacker, and analyze it in the next step.

### Flag

We can now construct the flag, with the information we found:
- Attacker IP address: `10.0.3.250`
- Attack method to log-in: `bruteforce`
- Plugin installed: `wp_webshell`
- Flag structure: `HACKDAY{attacker_ip:attack_method:plugin_installed}`

The flag is:
`HACKDAY{10.0.3.250:bruteforce:wp_webshell}`

Other flags were accepted, like `remote_code_execution`, `fuzzing`, `dirb`, `rce` or `webshell`.

## Creator

* Name: [Louis GAMBART](https://linkedin.com/in/louis-gambart)

## References

* [nginx documentation](https://nginx.org/en/docs/)
* [dirb](https://tools.kali.org/web-applications/dirb)
* [gobuster](https://tools.kali.org/web-applications/gobuster)
* [wordpress webshell](https://github.com/p0dalirius/Wordpress-webshell-plugin)
