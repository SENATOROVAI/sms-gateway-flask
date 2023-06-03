<?php
// Подключение к базе данных
$host = "localhost";
$username = "root";
$password = "";
$database = "SMSGATE";

try {
    $pdo = new PDO("mysql:host=$host;dbname=$database", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Ошибка подключения к базе данных: " . $e->getMessage());
}

// Функция для сохранения сообщения в базе данных
function saveMessage($modemPort, $phoneNumber, $message) {
    global $pdo;

    $sql = "INSERT INTO messages (modem_port, phone_number, message) VALUES (:modem_port, :phone_number, :message)";
    $statement = $pdo->prepare($sql);
    $statement->bindParam(':modem_port', $modemPort);
    $statement->bindParam(':phone_number', $phoneNumber);
    $statement->bindParam(':message', $message);
    $statement->execute();
}
?>
