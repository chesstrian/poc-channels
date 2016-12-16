$(document).ready(function () {
    var socket = new ReconnectingWebSocket('ws://' + window.location.host + window.location.pathname);

    socket.onmessage = function (message) {
        var data = JSON.parse(message.data);
        var chat = $('div#chat');

        var htmlMsg = '[' + data.datetime + '] ' + data.username + ': ' + data.message + '<br/>';

        chat.append(htmlMsg);
        chat.animate({scrollTop: $(document).height()}, 'slow');
    };

    var text = $('textarea#post');
    var button = $('button#send');
    var user = $('span#username').html();

    text.keydown(function (e) {
        if (e.which == 13) {
            if (e.ctrlKey) {
                text.val(text.val() + '\n');
            } else {
                e.preventDefault();
                button.click();
            }
        }
    });

    button.on('click', function () {
        var message = text.val();

        if (message != '') {
            socket.send(JSON.stringify({
                username: user,
                message: message
            }));
        }

        text.val('').focus();
        return null;
    });
});
