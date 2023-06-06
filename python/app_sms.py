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
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=None,
            database="smsgate"
        )
        return connection
    except:
        return "fail connect to db"
      
# if not hasattr(local_storage, 'connection'):
        # Создаем новое соединение для каждого потока
    #    local_storage.connection = sqlite3.connect('database.db')
    #return local_storage.connection

@app.route('/repeat', methods=['GET', 'POST'])
def repaet_send_sms():
    return "repaet"

@app.route('/delete', methods=['GET', 'POST'])
def delete_send_sms():
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM logs;"
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    delete_button  = "Таблица успешно удалена"
    return render_template('index.html', delete_button=delete_button)

@app.route('/', methods=['GET', 'POST'])
def send_sms():

    get_data = get_all_data()
    # modem_statuses = check_modem_status_command()
    # phone_numbers = "+998903256800 +998998766800"
    phone_numbers = request.form.get('phone_numbers','')

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
        # get_key_random_modem_port = random.choice(list(modemPorts))
        # get_val_random_modem_port = modemPorts[get_key_random_modem_port]

        
        # key_com = [key for key, value in modemPorts.items() if value == random_modem_port]        
            # Send SMS to each phone number using each modem
        
        # list_number = []
        
        for phone_numbers in phone_numbers.split():
            get_key_random_modem_port = random.choice(list(modemPorts))
            get_val_random_modem_port = modemPorts[get_key_random_modem_port]
            response = send_sms_command(get_val_random_modem_port, phone_numbers, message)
            # list_number.append(response)
            save_message(get_key_random_modem_port, phone_numbers, message, response)
            
        # response = send_sms_command(random_modem_port, phone_numbers, message)
            # delivery_results.append({
            #     'phone_number': phone_numbers,
            #     'modem_port': random_modem_port,
            #     'response': response
            # })

            # Insert message log into the database
        
        

            # Render the template and pass the delivery_results
            # return render_template('index.html',messages=get_data, delivery_results="", balance="", response=response)
        return render_template('index.html', get_data=get_data, response=response)

    # Render the initial form
    return render_template('index.html',get_data=get_data, response=response)

def save_message(get_key_random_modem_port,phone_number, message, status):
    # Save message to the database
    conn = get_db_connection()
    # get_imei = check_modem_status_command()
    cursor = conn.cursor()
    sql = "INSERT INTO `logs` (`id`, `imei`, `number`, `sms`, `status`) VALUES (NULL, %s, %s, %s, %s);"
    cursor.execute(sql, (get_key_random_modem_port, phone_number, message, status))
    conn.commit()
    cursor.close()
    conn.close()
    

def send_sms_command(gammurc, phone_numbers, message):
    # Run the Gammu command to send SMS using the specified modem
    command = f'C:\\Gammu\\bin\\gammu -c C:\\Gammu\\bin\\{gammurc} sendsms TEXT {phone_numbers} -text "{message}"'
    # return command
    try:
        output = subprocess.check_output(command, shell=True)
    
        return 1
    except subprocess.CalledProcessError as e:
        return f" {e.output.decode('utf-8').strip()}"

def check_modem_status_command(gammurc):
    pass
    # imei = {gammurc}
    
    # command = r"C:\Gammu\bin\gammu --identify"
    # try:
    #     output = subprocess.run(command, shell=True, capture_output=True, text=True)
    #     if output.returncode == 0:
    #         lines = output.stdout.strip().split('\n')
    #         imei_line = next((line for line in lines if 'IMEI' in line), None)
    #         if imei_line:
    #             imei = imei_line.split(':', 1)[1].strip()
    #             return imei
    #     else:
    #         return "imei Erorr, code 0"
    # except subprocess.CalledProcessError as e:
    #     return "Erorr C:\Gammu\bin\gammu --identify"

def get_all_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM `logs`')
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
    