from flask import Flask
from  drybreadcfg import global_cfg
import os
app = Flask(__name__)

@app.route('/suchar')
def get_dry_bread():
    return "Po co kotu telefon?" + " " + "Żeby MIAU"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', global_cfg['server']['port_number']))
    app.run(host=global_cfg['server']['host_name'], port=port)


