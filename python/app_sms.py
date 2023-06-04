from flask import Flask, render_template, request
import sqlite3
import subprocess
import random

app = Flask(__name__)

# Создаем соединение с базой данных
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Создаем таблицу 'messages', если она не существует
# cursor.execute('''CREATE TABLE IF NOT EXISTS messages
#                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                   modem_port TEXT,
#                   phone_number TEXT,
#                   message TEXT)''')
# conn.commit()

# Specify the list of modem ports
modemPorts = [
    "COM17",
    "COM11",
    "COM13",
    "COM14",
    "COM15",
    "COM17",
    "COM17",
    "COM17",
    "COM25",
    # Add the rest of the modem ports here
]


@app.route('/', methods=['GET', 'POST'])
def send_sms():
    if request.method == 'POST':
        phone_numbers = request.form.get('phone_numbers', '').strip()
        message = request.form.get('message', '')

        # Check modem status
        modem_statuses = {}
        for modem_port in modemPorts:
            status = check_modem_status_command(modem_port)
            modem_statuses[modem_port] = status
        # Check account balance
        balance = check_balance_command()
        # Array to store delivery results
        delivery_results = []
        random_modem_port = random.choice(modemPorts)
        if message or phone_numbers:
            # Send SMS to each phone number using each modem
            response = send_sms_command(random_modem_port, phone_numbers, message)
            delivery_results.append({
                'phone_number': phone_numbers,
                'modem_port': random_modem_port,
                'response': response
            })

            # Insert message log into the database
            save_message(random_modem_port, phone_numbers, message)

            # Render the template and pass the delivery_results
            return render_template('index.html', delivery_results=delivery_results, balance=balance, modem_statuses=modem_statuses)

    # Render the initial form
    return render_template('index.html')

def save_message(modem_port, phone_number, message):
    # Save message to the database
    sql = "INSERT INTO messages (modem_port, phone_number, message) VALUES (?, ?, ?)"
    cursor.execute(sql, (modem_port, phone_number, message))
    conn.commit()

def send_sms_command(modem_port, phone_numbers, message):
    # Run the Gammu command to send SMS using the specified modem
    command = f"C:\\Gammu\\bin\\gammu.exe -c gammurc sendsms TEXT {phone_numbers} -text {message}"
    try:
        output = subprocess.check_output(command, shell=True)
        return "SMS sent successfully"
    except subprocess.CalledProcessError as e:
        return f"Failed to send SMS. Error: {e.output.decode('utf-8').strip()}"

def check_modem_status_command(modem_port):
    command = f"C:\\Gammu\\bin\\gammu.exe -c gammurc identify"
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        error_output = e.output.decode('utf-8')
        raise Exception(f"Failed to check modem status. Error: {error_output}")

def check_balance_command():
    # Run the Gammu command to check account balance
    command = "C:\\Gammu\\bin\\gammu.exe -c gammurc getussd *107#"
    output = subprocess.check_output(command, shell=True)
    return output.decode('utf-8')


if __name__ == '__main__':
    app.run()
