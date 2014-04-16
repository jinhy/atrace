$('#insert').live('click',function(){
    data={}
    $(this).parent().find("td:lt("+$(this).index()+")").each(function(){
        data[$(this).attr("id")]=$(this).find('textarea').val();
    });
    a=$(this).parent();
    $.get(
        '/set',
        data,
        function (json, textStatus) {
            if (textStatus == 'success') {
                $("textarea").val("");
                a.next().clone(true).insertAfter(a);
                b=a.next();
                b.css({"display":"table-row","background-color": "gainsboro"});
                for(k in data)
                {
                    b.find("#"+k).text(data[k]);
                }
            }
        });
});
$('#edit').live('click',function(){
    $(this).parent().find("td:gt(0):lt("+($(this).index()-2)+")").each(function(){
        $(this).html("<textarea >"+$(this).text()+"</textarea>");
    });
    $(this).text("确定");
    $(this).attr("id","confirm");
    
});
$('#confirm').live('click',function(){
    data={}
    data["name"]=$(this).parent().find("td:eq(0)").text();
    $(this).parent().find("td:gt(0):lt("+($(this).index()-2)+")").each(function(){
        data[$(this).attr("id")]=$(this).find('textarea').val();
    });
    a=$(this);
    $.get(
        '/set',
        data,
        function (json, textStatus) {
            if (textStatus == 'success') {
                a.text("修改");
                a.attr("id","edit");
                for(k in data)
                {
                    a.parent().find("#"+k).text(data[k]);
                }
            }
        });
});
$('#delete').live('click',function(){
    var a=$(this).parent();
    $.get(
        '/delete',
        {'name': $(this).parent().find("#name").text()},
        function (json, textStatus) {
            if (textStatus == 'success') {
                a.remove();
                //if (json.ans.length > 0) map.setCenter(markersArray[0].getPosition());
            }
        });
});