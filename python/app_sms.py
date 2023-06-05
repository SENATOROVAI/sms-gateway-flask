from flask import Flask, render_template, request
import sqlite3
import subprocess
import random
import mysql.connector


app = Flask(__name__)
app.config['DEBUG'] = True


# # Создаем таблицу 'messages', если она не существует
# cursor.execute("""ALTER TABLE messages
# ADD COLUMN status VARCHAR(50) NULL;
# """)

# conn.commit()

# Specify the list of modem ports
modemPorts = {
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
    # Add the rest of the modem ports here
}

# Создаем локальное хранилище для каждого потока
#local_storage = threading.local()

# Функция для получения соединения с базой данных
def get_db_connection():
    # Создаем соединение с базой данных
    with sqlite3.connect('database.db') as conn:
        return conn


# if not hasattr(local_storage, 'connection'):
        # Создаем новое соединение для каждого потока
    #    local_storage.connection = sqlite3.connect('database.db')
    #return local_storage.connection

@app.route('/', methods=['GET', 'POST'])
def send_sms():
    get_data = get_all_data()
    modem_statuses = check_modem_status_command()
    phone_numbers = request.form.get('phone_numbers', '').strip()
    message = request.form.get('message', '')
    response = ""
    if request.method == 'POST' and phone_numbers and message:
        # Check modem status
        # modem_statuses = {}
        #for modem_port in modemPorts:
      #      modem_statuses[modem_port] = status
            # modem_statuses = ""

        # Check account balance
        # balance = check_balance_command()
        balance = ""
        # Array to store delivery results
        # delivery_results = []
        random_modem_port = random.choice(modemPorts)
        key_com = [key for key, value in modemPorts.items() if value == random_modem_port]        
            # Send SMS to each phone number using each modem
        response = send_sms_command(random_modem_port, phone_numbers, message)
            # delivery_results.append({
            #     'phone_number': phone_numbers,
            #     'modem_port': random_modem_port,
            #     'response': response
            # })

            # Insert message log into the database
        if response == "SMS sent successfully":
            save_message(key_com, phone_numbers, message, modem_statuses)

            # Render the template and pass the delivery_results
            # return render_template('index.html',messages=get_data, delivery_results="", balance="", response=response)
        return render_template('index.html', get_data=get_data, response=response)

    # Render the initial form
    return render_template('index.html',get_data=get_data, response=response)

def save_message(modem_port, phone_number, message, status):
    # Save message to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO messages (modem_port, phone_number, message, status) VALUES (?, ?, ?, ?)"
    cursor.execute(sql, (modem_port, phone_number, message, status))
    conn.commit()

def send_sms_command(modem_port, phone_numbers, message):
    # Run the Gammu command to send SMS using the specified modem
    command = f"C:\\Gammu\\bin\\gammu -c {gammurc} sendsms TEXT {phone_numbers} -text {message}"
    # match modem_port:
    #     case "COM17":
    #         command = f"C:\\Gammu\\bin\\gammu -c gammurc sendsms TEXT {phone_numbers} -text {message}"
    #     case "COM11":
    #         command = f"C:\\Gammu\\bin\\gammu -c gammurc sendsms TEXT {phone_numbers} -text {message}"
    #     case "COM12":
    #         command = f"C:\\Gammu\\bin\\gammu -c gammurc sendsms TEXT {phone_numbers} -text {message}"
    #     case "COM12":
    #         command = f"C:\\Gammu\\bin\\gammu -c gammurc sendsms TEXT {phone_numbers} -text {message}"
    #     case "COM13":
    #         command = f"C:\\Gammu\\bin\\gammu -c gammurc sendsms TEXT {phone_numbers} -text {message}"
    #     case "COM14":
    #         command = f"C:\\Gammu\\bin\\gammu -c gammurc sendsms TEXT {phone_numbers} -text {message}"
    #     case "COM15":
    #         command = f"C:\\Gammu\\bin\\gammu -c gammurc sendsms TEXT {phone_numbers} -text {message}"
    #     case "COM16":
    #         command = f"C:\\Gammu\\bin\\gammu -c gammurc sendsms TEXT {phone_numbers} -text {message}"
    #     case "COM18":
    #         command = f"C:\\Gammu\\bin\\gammu -c gammurc sendsms TEXT {phone_numbers} -text {message}"
    #     case "COM19":
    #         command = f"C:\\Gammu\\bin\\gammu -c gammurc sendsms TEXT {phone_numbers} -text {message}"
    #     case "COM20":
            
    try:
        output = subprocess.check_output(command, shell=True)
        return "SMS sent successfully"
    except subprocess.CalledProcessError as e:
        return f"Failed to send SMS."
               # f" {e.output.decode('utf-8').strip()}"

def check_modem_status_command():
    command = r"C:\Gammu\bin\gammu --identify"
    try:
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        if output.returncode == 0:
            lines = output.stdout.strip().split('\n')
            imei_line = next((line for line in lines if 'IMEI' in line), None)
            if imei_line:
                imei = imei_line.split(':', 1)[1].strip()
                return imei
        else:
            return None
    except subprocess.CalledProcessError as e:
        return None

def get_all_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM `messages`')
    rows = cursor.fetchall()
    return rows
# def check_balance_command():
#     command = 'C:\\Gammu\\bin\\gammu.exe -c gammurc getussd *107#'
#     try:
#         output = subprocess.check_output(command, shell=True)
#         result = output.decode('utf-8')
#         # Process the result
#         return result
#     except subprocess.CalledProcessError as e:
#         error_output = e.output.decode('utf-8')
#         return (f"Command '{command}' returned non-zero exit status {e.returncode}. Error: {error_output}")
    # Run the Gammu command to check account balance
    # command = "C:\\Gammu\\bin\\gammu.exe -c gammurc getussd *107#"
    # output = subprocess.check_output(command, shell=True)
    # return output.decode('utf-8')


if __name__ == '__main__':
    app.run()
    