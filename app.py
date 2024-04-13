from flask import Flask

app = Flask(__name__)

import controllers.main_page, controllers.classification, controllers.editor
