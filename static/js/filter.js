$(function () {
    $('.filter-form').on('submit', function (e) {

        var color = $('#color').val();
        var price = $('#price').val();
        var size = $('#size').val();
        var brand = $('#brand').val();
        console.log(color);
        console.log(price);
        console.log(size);
        console.log(brand);
        data = [color, price, size, brand]
        var filter_id = AjaxFilter(e, data);

    });
});

function AjaxFilter(e, data) {
    e.preventDefault();

    var order_id = '';
    var request = $.ajax({
        method: 'POST',
        url: filter_url,
        async: false,
        data: {
            color: data[0],
            price: data[1],
            size: data[2],
            brand: data[3],
            csrfmiddlewaretoken: csrf_token,
        }
    });
    request.done(function (data) {
        console.log("first done")
        location = data.url
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
};


