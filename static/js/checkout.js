$(function () {
    $('.order-form').on('submit', function (e) {
        var amount = parseFloat($('.order-form input[name="amount"]').val().replace(',', ''));
        var type = $('.order-form input[name="type"]:checked').val();
        var order_id = AjaxCreateOrder(e);
        if (order_id == false) {
            alert('주문 생성 실패\n다시 시도해주세요.');
            return false;
        }

        var merchant_id = AjaxStoreTransaction(e, order_id, amount, type);
        redirect_to_paypal(e, merchant_id)
        return false;
    });
});

function AjaxCreateOrder(e) {
    e.preventDefault();
    var order_id = '';
    var request = $.ajax({
        method: 'POST',
        url: order_create_url,
        async: false,
        data: $('.order-form').serialize()
    });
    request.done(function (data) {
        if (data.order_id) {
            order_id = data.order_id;
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
    return order_id;
}

function AjaxStoreTransaction(e, order_id, amount, type) {
    e.preventDefault();
    var merchant_id = '';
    var request = $.ajax({
        method: 'POST',
        url: order_checkout_url,
        async: false,
        data: {
            order_id: order_id,
            amount: amount,
            type: type,
            csrfmiddlewaretoken: csrf_token,
        }
    });
    request.done(function (data) {
        if (data.works) {
            merchant_id = data.merchant_id;
        }
    });
    request.fail(function (jqXHR, textStatus) {
        if (jqXHR.status == 404) {
            alert("페이지가 존재하지 않습니다.");
        } else if (jqXHR.status == 403) {
            alert("로그인 해주세요.");
        } else {
            alert("code:" + jqXHR.status + "\n" + "message:" + jqXHR.responseText + "\n");
            alert("문제가 발생했습니다.\n다시 시도해주세요.");
            console.log('here it is')
        }
    });
    return merchant_id;
}
function redirect_to_paypal(e, merchant_id) {
    e.preventDefault();
    var request = $.ajax({
        method: "POST",
        url: order_paypal_url,
        async: false,
        data: {
            merchant_id: merchant_id,
            csrfmiddlewaretoken: csrf_token
        }
    });
    request.done(function (data) {
        window.location.href = data.url;
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

}
