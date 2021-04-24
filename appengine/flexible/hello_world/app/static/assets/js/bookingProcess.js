function bookingProcess(url, contenedor) {
    $.get(url, {}, function (data) {
        $("#" + contenedor).html(data);
    });
}