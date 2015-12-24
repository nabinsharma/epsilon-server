import sys
sys.path.insert(0, "/var/www/epsilon-server/")

from dejavu import app as application
application.secret_key = "nothing secret here!"
