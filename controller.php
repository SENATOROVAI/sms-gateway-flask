<?php 
include "model.php";

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
            saveMessage($modemPort, $phoneNumber, $message);
        }
    }
} else {
    echo "Неверный метод запроса";
    exit;
}
?>

?>
