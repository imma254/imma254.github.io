jQuery(document).ready(function($) {
    $('button').on('click', function() {
        $('#loader').load($(this).data('href'));
    });
});

