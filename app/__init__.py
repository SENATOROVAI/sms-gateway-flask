from flask import Flask

app: Flask = Flask(__name__)

from .controllers.controller import SMSController
controller: SMSController = SMSController()

