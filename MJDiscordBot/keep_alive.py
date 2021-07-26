from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def main():
    return "Saki is ready."

def run():
    app.run(host="0.0.0.0", port=1688)

def keep_alive():
    server = Thread(target=run)
    server.start()