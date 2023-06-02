<!DOCTYPE html>
<html>
<head>
    <title>Отправка SMS</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>Отправка SMS</h1>

    <form id="smsForm">
        <label>Введите текст сообщения:</label><br>
        <textarea name="message" rows="4" cols="50"></textarea><br><br>

        <label>Выберите порт модема:</label><br>
    <?php for ($i = 0; $i < 10; $i++) : ?>
        <select name="modem_port[]">
            <option value="">Выберите порт</option>
            <option value="COM1">COM1</option>
            <option value="COM17">COM17</option>
            <option value="COM1">COM1</option>
            <option value="COM1">COM1</option>
            <option value="COM1">COM1</option>
            <option value="COM1">COM1</option>
            <option value="COM1">COM1</option>
            <option value="COM1">COM1</option>
            <option value="COM1">COM1</option>
            <option value="COM1">COM1</option>
        </select>

        <select name="modem_status[]">
            <option value="enabled">Включен</option>
            <option value="disabled">Выключен</option>
        </select>
        <br><br>
    <?php endfor; ?>

        // Отображение выбора порта модема для каждого модема
        foreach ($modemPorts as $index => $port) {
            echo "<label>Выберите порт модема для модема " . ($index + 1) . ":</label><br>";
            echo "<input type=\"hidden\" name=\"modem_port[]\" value=\"$port\">";
            echo "<select name=\"modem_status[]\">";
            echo "<option value=\"enabled\">Включен</option>";
            echo "<option value=\"disabled\">Выключен</option>";
            echo "</select><br><br>";
        }
        ?>

        <label>Введите номера получателей (каждый номер с новой строки):</label><br>
        <textarea name="phone_numbers" rows="4" cols="50"></textarea><br><br>

        <input type="submit" value="Отправить">
    </form>

    <div id="response"></div>

    <script>
        document.getElementById('smsForm').addEventListener('submit', function(event) {
            event.preventDefault();
            
            var form = event.target;
            var formData = new FormData(form);
            var xhr = new XMLHttpRequest();
            
            xhr.open('POST', 'send_sms.php', true);
            xhr.onload = function() {
                if (xhr.status === 200) {
                    var response = xhr.responseText;
                    document.getElementById('response').innerHTML = response;
                } else {
                    alert('Произошла ошибка при отправке запроса.');
                }
            };
            
            xhr.send(formData);
        });
    </script>
</body>
</html>
