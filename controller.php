<?php

// Function to send SMS using Gammu and a specified modem
function sendSMS($modemPort, $phoneNumber, $message)
{
    // Escape special characters in the phone number and message
    $phoneNumber = escapeshellarg($phoneNumber);
    $message = escapeshellarg($message);

    // Run the Gammu command to send SMS using the specified modem
    $command = "C:\Gammu\bin\gammu.exe -c gammurc sendsms TEXT {$phoneNumber} -text {$message}";
    exec($command, $output, $returnVar);

    if ($returnVar === 0) {
        return "SMS sent successfully";
    } else {
        return "Failed to send SMS";
    }
}

// Check if the form was submitted
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get the phone numbers and message from the form
    $phoneNumbers = explode("\n", $_POST['phone_numbers']);
    $message = $_POST['message'];

    // Remove any empty phone numbers
    $phoneNumbers = array_filter($phoneNumbers, function ($number) {
        return !empty(trim($number));
    });

    // Specify the list of modem ports
    $modemPorts = [
        "COM17",
        "COM2",
        // Add the rest of the modem ports here
    ];

    // Send SMS to each phone number using each modem
    foreach ($phoneNumbers as $phoneNumber) {
        $phoneNumber = trim($phoneNumber);

        foreach ($modemPorts as $modemPort) {
            $response = sendSMS($modemPort, $phoneNumber, $message);
            echo "<p>Sending SMS to {$phoneNumber} using {$modemPort}: {$response}</p>";
        }
    }
}
?>
