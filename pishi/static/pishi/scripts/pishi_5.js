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

    $(document.body).on('click', '.predict-btn', function () {
        let btnRow = $(this).closest('.predict-btn-row');
        btnRow.hide();
        btnRow.siblings('.predict-form-row').show();
    });

    $(document.body).on('click', '.predict-form-cancel-btn', function () {
        let formRow = $(this).closest('.predict-form-row');
        formRow.hide();
        formRow.siblings('.predict-btn-row').show();
    });

    $(document.body).on('change', '.predict-form', function () {
       let home_r = parseInt($(this).find('.home_result_prediction').val()),
           away_r = parseInt($(this).find('.away_result_prediction').val()),
           match_type = parseInt($(this).find('.match_type').val());
       if(home_r === 0 && away_r === 0 && match_type !== 0) {
           $(this).find('.home_penalty_prediction').prop('required', true);
           $(this).find('.away_penalty_prediction').prop('required', true);
           $(this).find('.penalty-predict-row').removeAttr('hidden');
           $(this).find('.penalty-predict-row').show();
       } else if(!isNaN(home_r) && !isNaN(away_r) && match_type !== 0 && (home_r !== 0 || away_r !== 0)) {
           $(this).find('.home_penalty_prediction').prop('required', false);
           $(this).find('.away_penalty_prediction').prop('required', false);
           $(this).find('.penalty-predict-row').hide();
       }
    });

    // $(document.body).on('submit', '.predict-form', function (e) {
    //     e.preventDefault();
    //     let home_r = parseInt($(this).find('.home_result_prediction').val()),
    //         away_r = parseInt($(this).find('.away_result_prediction').val()),
    //         match_pk = parseInt($(this).find('.match_pk').val()),
    //         match_type = parseInt($(this).find('.match_type').val());
    //     let data = {"home_r": home_r, "away_r": away_r, "match_pk": match_pk};
    //
    //     if(match_type !== 0 && home_r === 0 && away_r === 0) {
    //         data["home_p"] = parseInt($(this).find('.home_penalty_prediction').val());
    //         data["away_p"] = parseInt($(this).find('.away_penalty_prediction').val());
    //     }
    //     let parent_li = $(this).closest('li');
    //     $.post('/predict/', data)
    //         .done(function (result) {
    //             parent_li.html(result);
    //         })
    // });

    $(document.body).on('click', '.predict-edit-btn', function () {
        let parentRow = $(this).closest('.predict-edit-btn-row');
        parentRow.hide();
        parentRow.siblings('.predicted-info-div').hide();
        parentRow.siblings('.predict-form-row').show();

    });

    $(document.body).on('click', '.predict-edit-cancel-button', function () {
        let parentRow = $(this).closest('.predict-form-row');
        parentRow.siblings('.predicted-info-div').show();
        parentRow.siblings('.predict-edit-btn-row').show();
        parentRow.hide();
    });

    $(document.body).on('click', '#what_are_rules', function () {
        $('.scores-list').hide();
        $('.rules-container').show();
    });

    $(document.body).on('click', '#back_to_scores_icon', function () {
        $('.rules-container').hide();
        $('.scores-list').show();
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