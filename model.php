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

// Функция для сохранения сообщения в базе данных
function saveMessage($modemPort, $phoneNumber, $message) {
    global $mysqli;

    $sql = "INSERT INTO messages (modem_port, phone_number, message) VALUES (?, ?,
