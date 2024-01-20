from flask import Flask, render_template, request, redirect, url_for
import requests

flag = open("flag.txt").read()

SERVERS = ["https://hackday.fr/", "https://www.nasa.gov/"]
IDS = set()

def very_unique_id(ip_address):
    # Gives each server a unique ID
    acc = 0
    for c in ip_address:
        acc = (acc + ord(c)) % 42

    return acc

for server in SERVERS:
    IDS.add(very_unique_id(server)) # Allows for a way faster lookup

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for("home"))

@app.route('/home')
def home():
    return render_template('home.html', urls=SERVERS)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/send', methods=['POST'])
def send():
    ip_address = request.form['ip_address']
    if very_unique_id(ip_address) in IDS:
        requests.get(ip_address + flag)
        return render_template('home.html', urls=SERVERS, message="Sent request")
    else:
        return render_template('home.html', urls=SERVERS, message="No such server")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
