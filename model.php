<?php include "controller.php"; ?>
// Подключение к базе данных
$host = "localhost";
$username = "root";
$password = "";
$database = "SMSGATE";

$mysqli = new mysqli($host, $username, $password, $database);

if ($mysqli->connect_error) {
    die("Ошибка подключения к базе данных: " . $mysqli->connect_error);
}

// Функция для отправки SMS через Gammu
function sendSMSWithGammu($port, $phoneNumber, $message) {
    $command = "gammu-smsd-inject TEXT $phoneNumber -text \"$message\" -unicode -device $port";
    exec($command, $output, $returnVar);

    if ($returnVar === 0) {
        return "SMS отправлено успешно";
    } else {
        return "Ошибка при отправке SMS";
    }
}

// Обработка данных из формы
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $message = $_POST["message"];
    $modemPorts = $_POST["modem_port"];
    $modemStatuses = $_POST["modem_status"];
    $phoneNumbers = explode("\n", $_POST["phone_numbers"]);

    // Проверка наличия текста сообщения
    if (empty($message)) {
        echo "Введите текст сообщения";
        exit;
    }

    // Проверка наличия номеров получателей
    if (empty($phoneNumbers)) {
        echo "Введите хотя бы один номер получателя";
        exit;
    }

    // Отправка SMS для каждого модема
    for ($i = 0; $i < count($modemPorts); $i++) {
        $modemPort = $modemPorts[$i];
        $modemStatus = $modemStatuses[$i];

        // Проверка статуса модема
        if ($modemStatus !== "enabled") {
            continue; // Пропуск итерации, если модем выключен
        }

        // Проверка наличия порта модема
        if (empty($modemPort)) {
            continue; // Пропуск итерации, если порт модема не выбран
        }

        // Обработка каждого номера получателя
        foreach ($phoneNumbers as $phoneNumber) {
            $phoneNumber = trim($phoneNumber);

            // Проверка наличия номера получателя
            if (empty($phoneNumber)) {
                continue; // Пропуск итерации, если номер получателя пустой
            }

            // Отправка SMS через Gammu
            $response = sendSMSWithGammu($modemPort, $phoneNumber, $message);
            echo "<p>Отправка сообщения на номер $phoneNumber через модем $modemPort: $response</p>";

            // Сохранение информации о сообщении в базе данных
            $sql = "INSERT INTO messages (modem_port, phone_number, message) VALUES (?, ?, ?)";
            $statement = $mysqli->prepare($sql);
            $statement->bind_param("sss", $modemPort, $phoneNumber, $message);
            $statement->execute();
        }
    }
} else {
    echo "Неверный метод запроса";
    exit;
}

$mysqli->close();
?>
