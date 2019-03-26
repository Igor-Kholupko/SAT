$(document).on('submit', '#loginForm', function(event) {
    event.preventDefault();
    $.ajax({
        type: this.method,
        url: window.location.href,
        data: $(this).serialize(),
        success: function (response) {
            window.location.href = response['redirect'];
        },
        error: function (response) {
            let data = response.responseJSON;
            let keys = Object.keys(data);
            $('.errorlist').empty();
            $('#inputPassword').val('');
            for (let i = 0; i < keys.length; ++i) {
                let errorlist_selector = $('.errorlist.' + keys[i]);
                if (keys[i].startsWith('__') && keys[i].endsWith('__') || errorlist_selector.length === 0) {
                    $('.errorlist.nonfield').append("<li>" + data[keys[i]] + "</li>");
                } else {
                    errorlist_selector.append("<li>" + data[keys[i]] + "</li>");
                }
            }
        }
    });
});
