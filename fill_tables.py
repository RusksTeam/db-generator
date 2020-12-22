#### INFO: don't invoke this script directly. It's called from app.py/initialize
import json
from config import config as cfg
from api.models.drybread import DryBreadModel
from db import db

def has_any_tables(model_class):
    from db import db
    engine = db.get_engine(bind=model_class.__bind_key__)
    return model_class.metadata.tables[model_class.__tablename__].exists(engine)

#### drybreads database
def load_tables():
    if len(DryBreadModel.find_all()) == 0:
        print('Database does not exist/is empty. Creating from file...')
        data = dict()
        with open('tmp_database.json', 'r', encoding='utf-8') as f:
            data = json.loads(f.read())

        for e in data['suchary']:
            if e['type'] <= cfg['JOKE_TYPE']:
                db = DryBreadModel(e['q'], e['a'])
                db.save_to_db()

        print('drybreads loaded:', [x.json() for x in db.find_all()])

####users database
    from api.models.user import UserModel
    admin = UserModel('admin', 'admin', UserModel.ROLE_ADMIN)
    admin.save_to_db()