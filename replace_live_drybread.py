
from  drybreadcfg import global_cfg
import drybreadgenerator as dbg
from mmap import mmap
import sys
import platform
import os

if platform.system() == 'Windows':
    shm = mmap.mmap(0, 4, global_cfg['shared_mem']['drybread_tag'])
else:
    fd = os.open('/tmp/' + global_cfg['shared_mem']['drybread_tag'], os.O_CREAT | os.O_TRUNC | os.O_RDWR)
    shm = mmap.mmap(fd, 4, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE)


def reroll_drybread():
    db_index = dbg.get_random_drybread_index()
    shm.write(bytes([db_index]))
    shm.close()
    return db_index

def set_fixed_drybread(index):
    shm.write(bytes([index]))
    shm.close()

if __name__ == '__main__':
    try:
        if len(sys.argv) > 1:
            set_fixed_drybread(int(sys.argv[1]))
            print("New brybread index choosen:", sys.argv[1], file=sys.stderr)
        else:
            new_db_index = reroll_drybread()
            print("Rerolled. New brybread index:", new_db_index, file=sys.stderr)
    except:
        print("Something went wrong. Nothing has changed in dry bread runtime. Analyze yourself.\r\nUsage:\r\n" + sys.argv[0], " [new db index]\r\nYour command:", sys.argv, "\r\nTotal drybreads: ", dbg.NUM_DB, file=sys.stderr)