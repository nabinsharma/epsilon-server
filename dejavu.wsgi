activate_this = '/var/www/html/epsilon-server/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, '/var/www/epsilon-server')

from dejavu import app as application
