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
            success: function(data) {
                // Обработка успешного ответа сервера
                console.log(data)
                $("body").html(data);
            },
            error: function(error) {
                // Обработка ошибки
                console.log(error);
            }
        });
    });

    $('#delTable').submit(function(event) {
        event.preventDefault(); // Предотвращение отправки формы по умолчанию

        // Получение данных формы

        // Отправка AJAX-запроса
        $.ajax({
            url: '/delete',
            type: 'POST',
     
            success: function(response) {
                var resultText = $(response).find("#result");
                if (result) $("#result").text("Таблица успешно удалена");
                $("table").remove()
               
            },
            error: function(error) {
                // Обработка ошибки
                console.log(error);
            }
        });
    });
});