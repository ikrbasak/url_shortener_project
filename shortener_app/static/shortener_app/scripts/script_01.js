$(
    function () {
        const url_form = $('#url_form');
        const url_submit = $('#url_submit');
        const notification = $('#notification');
        const url_input = $('#url_input');
        const key_input = $('#key_input');

        notification.hide();

        url_form.on('submit', function (event) {
            event.preventDefault();
            url_submit.prop(
                {"disabled": true}
            )

            $.ajax({
                method: "POST",
                url: form_endpoint,
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": csrf_token,
                },
                data: $(this).serialize(),
                success: (data, textStatus, jqXHR) => {
                    navigator.clipboard.writeText('https://webhost1.pythonanywhere.com/' + data.key);
                    notification.addClass('success');
                    notification.removeClass('error');
                    notification.text('Short URL copied to clipboard');
                    notification.show();
                    url_form[0].reset();
                    setTimeout(() => {
                        url_input[0].focus();
                        notification.hide();
                    }, 1500);
                },
                error: (jqXHR, textStatus, errorThrown) => {
                    let response = jqXHR.responseJSON;

                    notification.removeClass('success');
                    notification.addClass('error');
                    notification.text(response.error_desc);
                    notification.show();
                    if (response.error_code === 'invalid_url') {
                        url_input[0].focus();
                    } else {
                        key_input[0].focus();
                    }
                    setTimeout(() => {
                        notification.hide();
                    }, 2000);
                },
                complete: (jqXHR, textStatus) => {
                    url_submit.prop(
                        {"disabled": false}
                    );
                }
            })
        })
    }
)
