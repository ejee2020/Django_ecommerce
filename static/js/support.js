$(function () {
    $('.support-form').on('submit', function (e) {
        AjaxCreateSupport(e);
        document.location.href = "/"
        return false;
    });
});

function AjaxCreateSupport(e) {
    e.preventDefault();
    var support_id = '';
    var request = $.ajax({
        method: 'POST',
        url: support_create_url,
        async: false,
        data: $('.support-form').serialize()
    });
    request.done(function (data) {
        if (data.support_id) {
            support_id = data.support_id;
        }

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
