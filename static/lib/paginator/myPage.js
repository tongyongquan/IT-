function exeData(num, type) {
    loadData(num);
    loadpage();
}
function loadpage() {
    var myPageCount = parseInt($("#PageCount").val());
    var myPageSize = parseInt($("#PageSize").val());
    var countindex = myPageCount % myPageSize > 0 ? (myPageCount / myPageSize) + 1 : (myPageCount / myPageSize);
    $("#countindex").val(countindex);

    var currentPage = parseInt($("#currentPage").val());
    var baseUrl = $("#baseUrl").val();


    $.jqPaginator('#pagination', {
        totalPages: parseInt($("#countindex").val()),
        visiblePages: parseInt($("#visiblePages").val()),
        currentPage: currentPage,
        first: '<li class="first"><a href="' + baseUrl + 1 + '">首页</a></li>',
        prev: '<li class="prev"><a href="' + baseUrl + (currentPage - 1) + '"><i class="arrow arrow2"></i>上一页</a></li>',
        next: '<li class="next"><a href="' + baseUrl + (currentPage + 1) + '">下一页<i class="arrow arrow3"></i></a></li>',
        last: '<li class="last"><a href="' + baseUrl + parseInt(countindex) + '">末页</a></li>',
        page: '<li class="page"><a href="' + baseUrl + '{{page}}'+'">{{page}}</a></li>',
    });
}
$(function () {
    loadData(43);
    loadpage();
});