#!/Users/smcho/virtualenv/riki/bin/python

# -*- coding: utf-8 -*-
import os

from flask_restful import Api

from wiki import create_app

directory = os.getcwd()
app = create_app(directory)


if __name__ == '__main__':
    app.run(port=80, debug=True)