$(document).ready(function() {
    $('#upload-form').submit(function(event) {
        event.preventDefault();  // Prevent the form from submitting the default way
        $('#loading').show();
        $(this).hide();

        var formData = new FormData(this);
        $.ajax({
            url: '/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                $('#loading').hide();
                $('#completed').show();
                $('#download-link').attr('href', response.download_url);
            },
            error: function() {
                $('#loading').hide();
                alert('An error occurred while processing the image.');
                $('#upload-form').show();
            }
        });
    });
});
