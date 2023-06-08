from flask import Flask
from controllers.controller import SMSController

app = Flask(__name__)
controller = SMSController()

@app.route('/repeat', methods=['GET', 'POST'])
def repeat_send_sms():
    return "repeat"


@app.route('/delete', methods=['GET', 'POST'])
def delete_send_sms():
    return controller.delete_send_sms()


@app.route('/send', methods=['GET', 'POST'])
def send_sms():
    return controller.send_sms()


@app.route('/', methods=['GET', 'POST'])
def main():
    return controller.get_data()

@app.route('/get', methods=['GET', 'POST'])
def get_db():
    return controller.download_csv()


match __name__:
    case "__main__":
        app.run(debug=True)
