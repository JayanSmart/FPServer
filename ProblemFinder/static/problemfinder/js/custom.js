/**
 * Created by adamedelberg on 2016/08/14.
 */
$(".dropdown-menu li a").click(function(){
  $(this).parents(".dropdown").find('.btn').html($(this).text() + ' <span class="caret"></span>');
  $(this).parents(".dropdown").find('.btn').val($(this).data('value'));
});


 function validate()
 {
     if(document.getElementById('q').value == "")
     {
         alert("fill db");
         return false;
     }
}