from app import app

from .controllers.controller import SMSController
controller: SMSController = SMSController()


@app.route("/repeat", methods=["GET", "POST"])
def repeat_send_sms() -> str:
    return "repeat"


@app.route("/delete", methods=["GET", "POST"])
def delete_send_sms() -> str:
    return controller.delete_send_sms()


@app.route("/send", methods=["GET", "POST"])
def send_sms() -> str:
    return controller.send_sms()


@app.route("/", methods=["GET", "POST"])
def main() -> str:
    return controller.get_data()


@app.route("/get", methods=["GET", "POST"])
def get_db() -> str:
    return controller.download_csv()
