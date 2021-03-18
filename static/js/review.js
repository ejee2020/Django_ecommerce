$(function () {
    $('.review-form').on('submit', function (e) {
        AjaxCreateReview(e);
        return false;
    });
});

function AjaxCreateReview(e) {
    e.preventDefault();
    var support_id = '';
    var request = $.ajax({
        method: 'POST',
        url: review_create_url,
        async: false,
        data: $('.review-form').serialize()
    });
    request.done(function (data) {
        alert("Review submitted successfully!")
        window.history.back();
    });
    request.fail(function (jqXHR, textStatus) {
        if (jqXHR.status == 404) {
            alert("페이지가 존재하지 않습니다.");
        } else if (jqXHR.status == 403) {
            alert("로그인 해주세요.");
        } else {
            alert("문제가 발생했습니다.\n다시 시도해주세요.");
        }
    });
    return support_id;
}
