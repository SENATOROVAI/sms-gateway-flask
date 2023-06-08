from app import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modem_port = db.Column(db.String(255))
    phone_number = db.Column(db.String(255))
    message = db.Column(db.Text)

    def __init__(self, modem_port, phone_number, message):
        self.modem_port = modem_port
        self.phone_number = phone_number
        self.message = message
