import sys, os

sys.path.insert(0, os.path.split(os.path.realpath(__file__))[0])

from manage import app

application = app
