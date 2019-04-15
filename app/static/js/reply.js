$(function () {
    $("a.reply").click(function(){
        var mess_id = $(this).parents(".top").siblings(".pass").val();
        var form = $("<form></form>").attr({"action":"/gbook","method":"post"}).addClass("replyForm");
        var textarea = $("<textarea></textarea>").attr({"cols":"50","rows":"5","name":"repcontent","required":"required"}).addClass("replyContent");
        var submit = $("<input>").attr({"type":"submit","value":"发送"});
        var pass_id = $("<input>").attr({"type":"hidden","value":mess_id,"name":"messid"});
        form.append(textarea);
        form.append(submit);
        form.append(pass_id);
        $(this).parents("div.top").siblings("div.input_reply").html(form);

    });


});