-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Июн 03 2023 г., 12:40
-- Версия сервера: 10.4.27-MariaDB
-- Версия PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `smsgate`
--

-- --------------------------------------------------------

--
-- Структура таблицы `messages`
--

CREATE TABLE `messages` (
  `id` int(11) UNSIGNED NOT NULL,
  `phone_number` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `modem_port` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `messages`
--

INSERT INTO `messages` (`id`, `phone_number`, `message`, `created_at`, `modem_port`) VALUES
(1, '+998903256800', 'asddddddd', '2023-06-02 21:30:39', '/dev/ttyUSB17'),
(2, '+998903256800', 'qwerty', '2023-06-02 21:33:12', 'COM17'),
(3, '+998903256800', '+998903256800', '2023-06-02 21:37:17', 'COM17'),
(4, '+998903256800', '+998903256800', '2023-06-02 21:50:43', 'COM17'),
(5, '+998903256800', '+998903256800', '2023-06-02 22:59:27', 'COM17'),
(6, '+998903256800', '+998903256800', '2023-06-02 22:59:41', 'COM17');

-- --------------------------------------------------------

--
-- Структура таблицы `sms_log`
--

CREATE TABLE `sms_log` (
  `id` int(11) NOT NULL,
  `phone_number` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `status` varchar(50) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `sms_log`
--

INSERT INTO `sms_log` (`id`, `phone_number`, `message`, `status`, `created_at`) VALUES
(1, '\"+998903256800\"', '\"+998903256800 new\"', 'Delivered', '2023-06-02 23:11:49'),
(2, '\"+998903256800\"', '\"+998903256800 new\"', 'Delivered', '2023-06-02 23:11:57');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`);

--
-- Индексы таблицы `sms_log`
--
ALTER TABLE `sms_log`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `messages`
--
ALTER TABLE `messages`
  MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT для таблицы `sms_log`
--
ALTER TABLE `sms_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
