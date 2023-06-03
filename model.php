<?php
// Подключение к базе данных
$host = "localhost";
$username = "root";
$password = "";
$database = "SMSGATE";

$mysqli = new mysqli($host, $username, $password, $database);

if ($mysqli->connect_error) {
    die("Ошибка подключения к базе данных: " . $mysqli->connect_error);
}



// Функция для сохранения сообщения в базе данных
function saveMessage($modemPort, $phoneNumber, $message) {
    global $mysqli;

    $sql = "INSERT INTO messages (modem_port, phone_number, message) VALUES (:modem_port, :phone_number, :message)";
    $statement = $mysqli->prepare($sql);
    $statement->bindParam(':modem_port', $modem_port);
    $statement->bindParam(':phone_number', $phone_number);
    $statement->bindParam(':message', $message);
    $statement->execute();
}
