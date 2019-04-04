/*
初始化页面搜索框数据
Author: fzjie
File: jquery.bootstrap-suggest
*/
$(document).ready(function () {
    $("#search").bsSuggest({
        url:"/api_stocklist",
        keyField:'a_ts_code',
        delayUntilKeyup: true,
        ignorecase: true,
        effectiveFieldsAlias:{a_ts_code: "代码",b_name:"名称",c_abbreviation:"简拼"},
        emptyTip: '暂无符合条件的股票',
        searchingTip: '搜索中...',
        showHeader: true,
        showBtn: false,
        clearable: true
    })
});
