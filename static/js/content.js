// $('.carousel').carousel()

//获取url中的参数
function getUrlParam(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
    var r = window.location.search.substr(1).match(reg); //匹配目标参数
    if (r != null) return unescape(r[2]);
    return 0; //返回参数值
}

$(function () {
    var nav = getUrlParam('nav');
    var children = $('#bs-example-navbar-collapse-8 > ul').children();
    var len = children.length - 1;
    nav = nav > len ? 0 : nav;
    $(children[nav]).addClass('active');
    // 导航条浮在最上面
    $(window).scroll(function () {
        var logo =$('.container').height();
        if ($(this).scrollTop()>logo) {
            $('#navbar').addClass('navbar-fixed-top');
        }else{
            $('#navbar').removeClass('navbar-fixed-top');
        }
    })
});

function loadData(num) {
    $("#PageCount").val(num.toString());
}

