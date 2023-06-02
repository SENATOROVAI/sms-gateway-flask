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

    $sql = "INSERT INTO messages (modem_port, phone_number, message) VALUES (?, ?, ?);
    $statement = $mysqli->prepare($sql);
    $statement->bind_param($modemPort, $phoneNumber, $message);
    $statement->execute();
}
