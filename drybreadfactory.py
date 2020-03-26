import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def get_dry_bread():
    return "Po co kotu telefon? Żeby MIAU"

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='localhost', port=port)





