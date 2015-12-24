from logging.handlers import RotatingFileHandler
import json
import logging
import os

from flask import Flask

import database
import dejavu_main

curr_dir = os.path.join(os.path.dirname(__file__))
top_dir = os.path.join(curr_dir, '..')
tmp_dir = os.path.join(top_dir, 'tmp')
config = {'ALLOWED_EXTENSIONS': ["mp3", "wav"],
          'UPLOAD_FOLDER': tmp_dir}

app = Flask(__name__)
app.secret_key = 'nothing_secret'

log_file = os.path.join(tmp_dir, 'epsilon-server.log')
log_file_handler = RotatingFileHandler(log_file,
                                       maxBytes=1024*1024*10,
                                       backupCount=10)
log_file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log_file_handler.setFormatter(formatter)
app.logger.addHandler(log_file_handler)

# Initialize db
db_cls = database.get_database()
with open(os.path.join(top_dir, 'dejavu.cnf'), 'r') as f:
    db_config_dict = json.load(f)
db = db_cls(**db_config_dict.get("database", {}))
    
djv = dejavu_main.Dejavu(db)


from dejavu import views
