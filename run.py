from flask import Flask
from  drybreadcfg import global_cfg
import drybreadgenerator as dbg
import os
import mmap
import platform
app = Flask(__name__)


print('Running on', platform.system(), 'system')
if platform.system() == 'Windows':
    shm = mmap.mmap(0, 4, global_cfg['shared_mem']['drybread_tag'])
else:#linux - for heroku
    db_index = dbg.get_random_drybread_index()
    with open('/tmp/' + global_cfg['shared_mem']['drybread_tag']) as f:
        f.write(str(db_index))
    fd = os.open('/tmp/' + global_cfg['shared_mem']['drybread_tag'], os.O_CREAT | os.O_TRUNC | os.O_RDWR)
    shm = mmap.mmap(fd, 0, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE)


@app.before_first_request
#def load_first_drybread():
#    shm.write(bytes([db_index]))
#    shm.seek(0)

@app.route('/suchar')
def display_drybread():
    db_index = int.from_bytes(shm.readline(), 'little')
    shm.seek(0)
    current_drybread = dbg.get_drybread_at_index(db_index)
    return '<h1>' + current_drybread['q'] + "</h1><h1>" + current_drybread['a'] + "</h1>"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', global_cfg['server']['port_number']))
    app.run(host=global_cfg['server']['host_name'], port=port)


