$(document).ready(function() {
    // Обработка отправки формы через AJAX
    $('#sms-form').submit(function (event) {
        event.preventDefault(); // Предотвращение отправки формы по умолчанию

        // Получение данных формы
        var formData = $(this).serialize();

        // Отправка AJAX-запроса
        $.ajax({
            url: '/',
            type: 'POST',
            data: formData,
            beforeSend: function() {
                // Действия перед отправкой запроса
                $('#sms-form button[type="submit"]').attr('disabled', true);
                $('#sms-form button[type="submit"]').html('Sending...');
            },
            success: function(data) {
                // Обработка успешного ответа сервера
                console.log(data);
                $("body").html(data);
            },
            error: function(error) {
                // Обработка ошибки
                console.log(error);
            },
            complete: function() {
                // Действия после выполнения запроса (в любом случае)
                $('#sms-form button[type="submit"]').attr('disabled', false);
                $('#sms-form button[type="submit"]').html('Send');
            }
        });
    });

    $('#delTable').submit(function(event) {
        event.preventDefault(); // Предотвращение отправки формы по умолчанию

        // Отправка AJAX-запроса
        $.ajax({
            url: '/delete',
            type: 'POST',
            beforeSend: function() {
                // Действия перед отправкой запроса
                $('#delTable button[type="submit"]').attr('disabled', true);
                $('#delTable button[type="submit"]').html('Deleting...');
            },
            success: function(response) {
                // Обработка успешного ответа сервера
                var resultText = $(response).find("#result");
                if (resultText) {
                    $("#result").text("Table successfully deleted");
                }
                $("table").remove();
            },
            error: function(error) {
                // Обработка ошибки
                console.log(error);
            },
            complete: function() {
                // Действия после выполнения запроса (в любом случае)
                $('#delTable button[type="submit"]').attr('disabled', false);
                $('#delTable button[type="submit"]').html('Delete Table');
            }
        });
    });
});
