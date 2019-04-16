$(function () {

    function hide_sel(){
        $("[name='recommend']").hide();
    }

   $("[name='list']").change(function(){
       if ($(this).val() >= 2){
         $("[name='recommend']").show();
       }
   });

     $("[name='list']").change(function(){
       if ($(this).val() == 1){
         $("[name='recommend']").hide();
       }
   });

    hide_sel();
});

