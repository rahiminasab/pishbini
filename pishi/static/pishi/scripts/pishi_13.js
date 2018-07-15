(function () {

    /* get the browser's stored cookie */
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    $(document.body).on('click', '#nav-predictions-tab', function () {
        $('#scoreboard').hide();
        $('#predictions').show();
    });

    $(document.body).on('click', '#nav-scoreboard-tab', function () {
        $('#predictions').hide();
        $('#scoreboard').show();
    });

    $(document.body).on('click', '.show-prediction-form-btn', function () {
        let btnRow = $(this).closest('.show-prediction-form-btn-row');
        btnRow.hide();
        btnRow.siblings('.predict-form').show();
    });

    $(document.body).on('click', '.predict-form-cancel-btn', function () {
        let formRow = $(this).closest('.predict-form');
        formRow.hide();
        formRow.siblings('.show-prediction-form-btn-row').show();
    });

    $(document.body).on('change', '.predict-form', function () {
       let home_result = parseInt($(this).find('input[name=home_result]').val()),
           away_result = parseInt($(this).find('input[name=away_result]').val()),
           match_type = parseInt($(this).find('input[name=match_type]').val());

       if(home_result === away_result && match_type !== 0) {
           $(this).find('input[name=home_penalty]').prop('required', true);
           $(this).find('input[name=away_penalty]').prop('required', true);
           $(this).find('.penalty-predict-row').show();
       } else if(!isNaN(home_result) && !isNaN(away_result) && match_type !== 0 && !(home_result === away_result)) {
           $(this).find('input[name=home_penalty]').prop('required', false).attr('value', '');
           $(this).find('input[name=away_penalty]').prop('required', false).attr('value', '');
           $(this).find('.penalty-predict-row').hide();
       }
    });

    $(document.body).on('submit', '.predict-form', function (e) {
        e.preventDefault();
        let match_list_item = $(this).closest('li');
        let route = $(this).attr('action');
        $.post(route, $(this).serialize())
            .done(function (data) {
                match_list_item.html(data);
            });
    });

    $(document.body).on('click', '.match-set-card', function () {
        let route = $(this).attr("data-route");
        window.location.replace(route);
    });

    $(document.body).on('click', '.match-list-header i', function () {
        let matchesContainer = $('#matches_container');
        let cardsContainer = matchesContainer.siblings('.card-columns');
        matchesContainer.hide();
        $('#initial-start-message-wrapper').show();
        cardsContainer.show();
    });

    let card_colors = [{"c": "white", "bg-c": "#650000", "title-c": "#ff9800"}, {"c": "#231919", "bg-c": "#e9d3ff", "title-c": "#6151b9" },
        {"c": "floralwhite", "bg-c": "#ef2c00", "title-c": "#e4f12c"} ];

    $('.match-set-info')
        .each(function (i) {
            $(this).css("background-color", card_colors[i%card_colors.length]["bg-c"])
                .css("color", card_colors[i%card_colors.length]["c"]);
            $(this).find('.card-title').css("color", card_colors[i%card_colors.length]["title-c"]);
        });

    $(window).ready(function() {
        $('.loading').hide();
    });

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

})();