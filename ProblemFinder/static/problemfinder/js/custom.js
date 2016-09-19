/**
 * Custom Javascript implementations
 * Date: 23 September 2016
 */

/* Function to change dropdown menus to display selected item */
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

