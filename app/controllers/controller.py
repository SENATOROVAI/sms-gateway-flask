import subprocess

from flask import render_template, request, Response
from models.model import MessageLogModel

import csv
from io import StringIO


class SMSController:
    def __init__(self) -> None:
        self.message_log_model: MessageLogModel = MessageLogModel()

    def send_sms_command(self, gammurc:srt, phone_number:str, message:str)->str:
        command:str = f'C:\\Gammu\\bin\\gammu -c C:\\Gammu\\bin\\{gammurc} sendsms TEXT {phone_number} -text "{message}"'
        try:
            subprocess.check_output(command, shell=True)
            return 1
        except subprocess.CalledProcessError as e:
            return f" {e.output.decode('utf-8').strip()}"

    def get_random_modem_port(self)->dict:
        modem_ports:dict = {
            "COM17": "gammurc",
            "COM11": "gammurc1",
            "COM13": "gammurc2",
            "COM14": "gammurc3",
            "COM15": "gammurc4",
            "COM17": "gammurc5",
            "COM17": "gammurc6",
            "COM17": "gammurc7",
            "COM25": "gammurc8",
            "COM25": "gammurc9",
        }
        return modem_ports

    def send_sms(self)->list:
        list_num: list = []
        numbers: list = [
            11231,
            1231231,
            21323123,
            1222312,
            12131,
            2131231,
            2111,
            2313,
            123123,
            123123,
        ]
        modem_ports: dict = {
            "COM17": "gammurc",
            "COM11": "gammurc1",
            "COM13": "gammurc2",
            "COM14": "gammurc3",
            "COM15": "gammurc4",
            "COM17-1": "gammurc5",
            "COM17-2": "gammurc6",
            "COM17-3": "gammurc7",
            "COM25": "gammurc8",
            "COM25-1": "gammurc9",
        }

        modem_index: int = 0  # переменная для отслеживания текущего индекса модема

        for number in numbers:
            modem_port: str = list(modem_ports)[
                modem_index % len(modem_ports)
            ]  # выбор модема по текущему индексу
            modem_index += 1  # увеличение индекса модема на 1
            list_num.append([number, [modem_port, "-", modem_ports[modem_port]]])
        return list_num

        get_data = self.message_log_model.get_data()
        if request.method == "POST":
            phone_numbers = request.form.get("phone_numbers")
            message = request.form.get("message")

            if phone_numbers and message:
                for phone_number in phone_numbers.split():
                    random_modem_port = self.get_random_modem_port()
                    response = self.send_sms_command(
                        random_modem_port, phone_number, message
                    )
                    self.message_log_model.save_message(
                        random_modem_port, phone_number, message, response
                    )

                return render_template(
                    "index.html", get_data=get_data, response=response
                )

        return render_template("index.html", get_data=get_data, response=response)

    def get_data(self)-str:
        get_data = self.message_log_model.get_data()
        return render_template("index.html", get_data=get_data)

    def download_csv(self)->Response:
        result = self.message_log_model.get_data()

        fieldnames: list = ["id", "imei", "number", "sms", "status"]

        csv_data = StringIO()
        writer = csv.DictWriter(csv_data, fieldnames=fieldnames)

        writer.writeheader()

        for row in result:
            writer.writerow(dict(zip(fieldnames, row)))

        response = Response(csv_data.getvalue(), mimetype="text/csv")
        response.headers.set("Content-Disposition", "attachment", filename="data.csv")

        return response

    def delete_send_sms(self)->str:
        self.message_log_model.delete_messages()
        delete_button: str = "Таблица успешно удалена"
        return render_template("index.html", delete_button=delete_button)
