from logging.handlers import RotatingFileHandler
import json
import logging

from flask import Flask

import database
import dejavu_main

config = {'ALLOWED_EXTENSIONS': ["mp3", "wav"],
          'UPLOAD_FOLDER': "./tmp"}

app = Flask(__name__)
app.secret_key = 'nothing_secret'

log_file_handler = RotatingFileHandler('epsilon-server.log',
                                       maxBytes=1024*1024*10,
                                       backupCount=10)
log_file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log_file_handler.setFormatter(formatter)
app.logger.addHandler(log_file_handler)

# Initialize db
db_cls = database.get_database()
with open(r'./dejavu.cnf') as f:
    db_config_dict = json.load(f)
db = db_cls(**db_config_dict.get("database", {}))

djv = dejavu_main.Dejavu(db)


from dejavu import views
