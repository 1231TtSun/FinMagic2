/*
初始化stock_prediction_base模板
Author: fzjie
File: jquery.stock_prediction_base
*/
$(document).ready(function () {
// activate the stock_prediction menu in based on url
    $("#stock_prediction_navigation a").each(function () {
        var pageUrl = window.location.href.split(/[?#]/)[0];
        var this_url=this.href.split(/[?#]/)[0];
        if ( this_url== pageUrl) {
            $(this).addClass("active");
        }
    });
});
