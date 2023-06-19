from http.client import responses
import subprocess
from typing import Optional

from flask import render_template, request, Response, redirect
from ..models.model import MessageLogModel

import csv
from io import StringIO

import asyncio

import concurrent.futures

# from asyncio import run


class SMSController:
    def __init__(self) -> None:
        self.message_log_model: MessageLogModel = MessageLogModel()

    def get_random_modem_port(self) -> dict:
        modem_ports: dict = {
            "COM1": "gammurc",
            "COM2": "gammurc1",
            # "COM3": "gammurc2",
            "COM4": "gammurc3",
            "COM5": "gammurc4",
            # "COM6": "gammurc5",
            # "COM7": "gammurc6",
            # "COM8": "gammurc7",
            # "COM9": "gammurc8",
            # "COM10": "gammurc9",
        }
        return modem_ports

    def send_sms_command(self, gammurc: str, phone_number: str, message: str) -> str:
        command: str = f'C:\\Gammu\\bin\\gammu -c C:\\Gammu\\bin\\{gammurc} sendsms TEXT {phone_number} -len 400 -unicode -text "{message}"'
        process = subprocess.run(command, shell=True, capture_output=True, text=True)

        if process.returncode == 0:
            return "ok"
        else:
            return process.stdout.strip()


    def send_sms(self) -> list:
        data_to_csv: List = []
        modem_index: int = 0  # переменная для отслеживания текущего индекса модема

        if request.method == "POST":
            phone_numbers = request.form.get("phone_numbers")
            message = request.form.get("message")

            if phone_numbers and message:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                
                    for phone_number in phone_numbers.split():
                        modem_port: str = list(self.get_random_modem_port())[
                            modem_index % len(self.get_random_modem_port())
                        ]
                        modem_index += 1

                        future = executor.submit(
                            self.send_sms_command,
                            self.get_random_modem_port()[modem_port],
                            phone_number,
                            message,
                        )
                       

                        data_to_csv.append(
                            {
                                "modem_port": modem_port,
                                "phone_number": phone_number,
                                "message": message,
                                "response": future.result(),
                            }
                        )

        for data in data_to_csv:
            modem_port = data["modem_port"]
            phone_number = data["phone_number"]
            message = data["message"]
            response = data["response"]
            self.message_log_model.save_message(
                modem_port, phone_number, message, response
            )

            # return redirect("/")

    def get_data(self) -> str:
        get_data = self.message_log_model.get_data()
        return render_template("index.html", get_data=get_data)

    def download_csv(self) -> Response:
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

    def delete_send_sms(self) -> str:
        self.message_log_model.delete_messages()
        # delete_button: str = "Таблица успешно удалена"
        return redirect("/")
