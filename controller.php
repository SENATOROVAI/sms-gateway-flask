<?php
include "model.php";

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get the phone numbers and message from the form
    $phoneNumbers = array_filter(array_map('trim', explode("\n", $_POST['phone_numbers'])));
    $message = $_POST['message'];

    // Array to store delivery results
    $deliveryResults = [];

    // Check account balance and display it in the footer
    $accountBalance = checkBalance();
    echo "<p>{$accountBalance}</p>";
    
    // Specify the list of modem ports
$modemPorts = [
    "COM17",
    "COM11",
    "COM13",
    "COM14",
    "COM15",
    "COM17",
    "COM17",
    "COM17",
    "COM25",
    // Add the rest of the modem ports here
];

    // Send SMS to each phone number using each modem
    foreach ($phoneNumbers as $phoneNumber) {
        foreach ($modemPorts as $modemPort) {
            $response = sendSMS($modemPort, $phoneNumber, $message);
            echo "<p>Sending SMS to {$phoneNumber} using {$modemPort}: {$response}</p>";

            // Insert message log into the database
            saveMessage($phoneNumber, $message, $response);

            // Store delivery result
            $deliveryResults[] = [
                'phone_number' => $phoneNumber,
                'modem_port' => $modemPort,
                'response' => $response
            ];
        }
    }

    // Display delivery results in a table
    echo "<table>";
    echo "<tr><th>Phone Number</th><th>Modem Port</th><th>Delivery Status</th></tr>";

    foreach ($deliveryResults as $result) {
        echo "<tr>";
        echo "<td>{$result['phone_number']}</td>";
        echo "<td>{$result['modem_port']}</td>";
        echo "<td>{$result['response']}</td>";
        echo "</tr>";
    }

    echo "</table>";
}

// Function to send SMS using Gammu and a specified modem
function sendSMS($modemPort, $phoneNumber, $message)
{
    // Escape special characters in the phone number and message
    $phoneNumber = escapeshellarg($phoneNumber);
    $message = escapeshellarg($message);

    // Run the Gammu command to send SMS using the specified modem
    $command = "C:\\Gammu\\bin\\gammu.exe -c gammurc sendsms TEXT {$phoneNumber} -text {$message}";
    exec($command, $output, $returnVar);

    return ($returnVar === 0) ? "SMS sent successfully" : "Failed to send SMS";
}

// Function to check modem status
function checkModemStatus($modemPort)
{
    // Run the Gammu command to check modem status
    $command = "C:\\Gammu\\bin\\gammu.exe -c gammurc identify";
    exec($command, $output, $returnVar);

    return ($returnVar === 0) ? implode("\n", $output) : "Failed to check modem status";
}

// Function to check account balance
function checkBalance()
{
    // Run the Gammu command to check account balance
    $command = "C:\\Gammu\\bin\\gammu.exe -c gammurc getussd *107#";
    exec($command, $output, $returnVar);

    return ($returnVar === 0) ? implode("\n", $output) : "Failed to check account balance";
}

// Check modem status
$modemStatuses = [];
foreach ($modemPorts as $modemPort) {
    $modemStatuses[$modemPort] = checkModemStatus($modemPort);
}

// Check if the form was submitted



// OLD CODE
// // Обработка данных из формы
// if ($_SERVER["REQUEST_METHOD"] === "POST") {
//     $message = $_POST["message"];
//     $modemPorts = $_POST["modem_port"];
//     $modemStatuses = $_POST["modem_status"];
//     $phoneNumbers = explode("\n", $_POST["phone_numbers"]);

//     // Проверка наличия текста сообщения
//     if (empty($message)) {
//         echo "Введите текст сообщения";
//         exit;
//     }

//     // Проверка наличия номеров получателей
//     if (empty($phoneNumbers)) {
//         echo "Введите хотя бы один номер получателя";
//         exit;
//     }

//     // Отправка SMS для каждого модема
//     for ($i = 0; $i < count($modemPorts); $i++) {
//         $modemPort = $modemPorts[$i];
//         $modemStatus = $modemStatuses[$i];

//         // Проверка статуса модема
//         if ($modemStatus !== "enabled") {
//             continue; // Пропуск итерации, если модем выключен
//         }

//         // Проверка наличия порта модема
//         if (empty($modemPort)) {
//             continue; // Пропуск итерации, если порт модема не выбран
//         }

//         // Обработка каждого номера получателя
//         foreach ($phoneNumbers as $phoneNumber) {
//             $phoneNumber = trim($phoneNumber);

//             // Проверка наличия номера получателя
//             if (empty($phoneNumber)) {
//                 continue; // Пропуск итерации, если номер получателя пустой
//             }

//             // Отправка SMS через Gammu
//             $response = sendSMSWithGammu($modemPort, $phoneNumber, $message);
//             echo "<p>Отправка сообщения на номер $phoneNumber через модем $modemPort: $response</p>";

//             // Сохранение информации о сообщении в базе данных
//             saveMessage($modemPort, $phoneNumber, $message);
//         }
//     }
// } else {
//     echo "Неверный метод запроса";
//     exit;
// }

// // Функция для отправки SMS через Gammu
// function sendSMSWithGammu($port, $phoneNumber, $message) {
//     $command = "gammu-smsd-inject TEXT $phoneNumber -text \"$message\" -unicode -device \"$port\"";
//     exec($command, $output, $returnVar);

//     if ($returnVar === 0) {
//         return "SMS отправлено успешно";
//     } else {
//         return "Ошибка при отправке SMS";
//     }
// }
?>
