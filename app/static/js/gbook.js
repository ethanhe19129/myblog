$(function () {

    function load_message(){
        $.ajax({
            url:'/getmessage',
            type:'get',
            dataType:'json',
            async:false,
            success:function(data){
                var html = "";
                $.each(data,function(i,obj){
                    html += "<ol class='commentlist'>";
                    html += "<li><div class='top'><span style='font-weight: bold;color:#3f3f3f' class='url'>"+obj.user_uname+"</span>";
                    html += "<span class='time'> @<a href='#' title=''>"+obj.pub_date+"</a>";
                    html += "<a href='#' class='replyComment'>发表</a>";
                    html += "<a style='float:right;cursor:default;' id='reply'>回复</a></span></div>";
                    html += "<div class='body'><p>"+obj.content+"</p></div>";
                    html += "<div class='input_reply'></div></li></ol>";
                    load_replymess(obj.id);
                });
                $(".commentstitle").after(html);

            }
        })

    }
       function load_replymess(mess_id){
        $.ajax({
            url:'/getreplymess',
            data:"mess_id="+mess_id,
            type:'get',
            dataType:'json',
            success:function(data){
                var html = "";
                $.each(data,function(i,obj){
                    html += "<li><div class='reply'><div class='top'>";
                    html += "<span class='url'>"+obj.user_uname+"</span>";
                    html += "<span class='time'>@ <a href='#' title=''>"+obj.pub_date+"</a>";
                    html += "<a href='#' class='replyComment'>回复</a></span></div>";
                    html += "<div class='body'>"+obj.content+"</div></div></li>";
                });
                $("#message").after(html);
            }
        })
    }


    load_message();
});

