<?php

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
<!-- HTML form -->
<!DOCTYPE html>
<html>
<head>
    <title>Send SMS</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>Send SMS</h1>

    <form method="POST">
        <label>Enter recipient phone numbers (one number per line):</label><br>
        <textarea name="phone_numbers" rows="4" cols="50"></textarea><br><br>

        <label>Enter message:</label><br>
        <textarea name="message" rows="4" cols="50"></textarea><br><br>

        <input type="submit" value="Send">
    </form>
</body>
</html>

            
            
