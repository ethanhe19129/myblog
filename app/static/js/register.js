$(document).ready(function(){
   $("#secondpwd").blur(function(){
       var firstpwd = $("#firstpwd").val();
       var secondpwd = $("#secondpwd").val();
       if (firstpwd!=secondpwd&&firstpwd.length!=0&&secondpwd.length!=0){
           $("#tip").html("两次密码输入不一致");
       }
   });

   window.loginname = 0;
   window.username = 0;
   window.email = 0;
   $("[name='loginname']").blur(function(){
       var newlogname = $(this).val().trim();
       $.get('/lognametest','loginname='+newlogname,function(data){
           if (!data.status&&newlogname.length!=0){
               $("#testname").html(data.msg).css({"color":"red","margin-left":"10px","font-size":"14px"});
           }else if (data.status&&newlogname.length!=0) {
               var tip = data.msg;
               $("#testname").html(data.msg).css({"color": "green", "margin-left": "10px", "font-size": "14px"});
           }
           window.loginname = data.status;
       },'json');
   });

     $("[name='username']").blur(function(){
       var uname = $(this).val().trim();
       $.get('/unametest','username='+uname,function(data){
           if (!data.status&&uname.length!=0){
               $("#testuser").html(data.msg).css({"color":"red","margin-left":"10px","font-size":"14px"});
           }else if (data.status&&uname.length!=0) {
               var tip = data.msg;
               $("#testuser").html(data.msg).css({"color": "green", "margin-left": "10px", "font-size": "14px"});
           }
           window.username = data.status;
       },'json');
   });

     $("[name='email']").blur(function(){
       var mail = $(this).val().trim();
       $.get('/emailtest','email='+mail,function(data){
           if (!data.status&&mail.length!=0){
               $("#testemail").html(data.msg).css({"color":"red","margin-left":"10px","font-size":"14px"});
           }else if (data.status&&mail.length!=0) {
               var tip = data.msg;
               $("#testemail").html(data.msg).css({"color": "green", "margin-left": "10px", "font-size": "14px"});
           }
           window.email = data.status;
       },'json');
   });

   $("form").submit(function(){
       if (window.loginname == 0 || window.username == 0 || window.email == 0){
           return false;
       }
       return true;
   });


});

