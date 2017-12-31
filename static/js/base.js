/**
 * Created by TF on 2017/12/29.
 */

//获取url中的参数
function getUrlParam(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
    var r = window.location.search.substr(1).match(reg); //匹配目标参数
    if (r != null) return unescape(r[2]);
    return 0; //返回参数值
}

$(function () {
    // 导航条浮在最上面
    $(window).scroll(function () {
        var logo =$('.container').height();
        if ($(this).scrollTop()>logo) {
            $('#navbar').addClass('navbar-fixed-top');
        }else{
            $('#navbar').removeClass('navbar-fixed-top');
        }
    })

    var children = $('#bs-example-navbar-collapse-8 ul li');
    $(children).click(function () {
        if($(this).hasClass('active')){
            return false;
        }
    })

});
