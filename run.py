from flask import Flask, render_template, request, redirect, url_for, flash
from  drybreadcfg import global_cfg
from hashlib import sha224
import drybreadgenerator as dbg
import os
import mmap
import platform

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my turbo secret key 948553098759874mfdnjeoiu'
current_drybread = dbg.get_random_drybread()

@app.route('/suchar')
@app.route('/')
def display_drybread():
    return render_template('suchar.html', q = current_drybread['q'], a = current_drybread['a'])

@app.route('/reroll', methods = ['POST', 'GET'])
def reroll_drybread():
    if request.method == 'POST':
        key_hash = sha224(request.form['key'].encode('utf-8')).hexdigest()
        if key_hash == '4135e2a7743f8d4345c66ff79440dd20ddfe76af91aed8b8d9c0dc61':
            global current_drybread
            current_drybread = dbg.get_random_drybread()
            flash('Drybread has been successfully rerolled.')
        else:
            flash("Wrong key. Did not reroll.")
        return redirect(url_for('display_drybread'))

    else:
        return render_template('reroll.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', global_cfg['server']['port_number']))
    app.run(host = global_cfg['server']['host_name'], port = port)


