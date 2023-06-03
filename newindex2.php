<?php

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

// Check modem status
$modemStatuses = [];
foreach ($modemPorts as $modemPort) {
    $modemStatuses[$modemPort] = checkModemStatus($modemPort);
}

// Check if the form was submitted
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get the phone numbers and message from the form
    $phoneNumbers = array_filter(array_map('trim', explode("\n", $_POST['phone_numbers'])));
    $message = $_POST['message'];

    // Array to store delivery results
    $deliveryResults = [];

    // Check account balance and display it in the footer
    $accountBalance = checkBalance();
    echo "<p>{$accountBalance}</p>";

    // Send SMS to each phone number using each modem
    foreach ($phoneNumbers as $phoneNumber) {
        foreach ($modemPorts as $modemPort) {
            $response = sendSMS($modemPort, $phoneNumber, $message);
            echo "<p>Sending SMS to {$phoneNumber} using {$modemPort}: {$response}</p>";

            // Insert message log into the database
            insertMessageLog($phoneNumber, $message, $response);

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
?>

<!-- HTML form -->
<!DOCTYPE html>
<html>
<head>
    <title>Send SMS</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>Send SMS</h1>

    <table>
        <tr>
            <th>Modem Port</th>
            <th>Status</th>
        </tr>
        <?php foreach ($modemPorts as $modemPort): ?>
            <tr>
                <td><?php echo $modemPort; ?></td>
                <td><?php echo isset($modemStatuses[$modemPort]) ? $modemStatuses[$modemPort] : "Unknown"; ?></td>
            </tr>
        <?php endforeach; ?>
    </table>

    <form method="POST">
        <label>Enter recipient phone numbers (one number per line):</label><br>
        <textarea name="phone_numbers" rows="4" cols="50"></textarea><br><br>

        <label>Enter message:</label><br>
        <textarea name="message" rows="4" cols="50"></textarea><br><br>

        <input type="submit" value="Send">
    </form>
</body>
</html>
