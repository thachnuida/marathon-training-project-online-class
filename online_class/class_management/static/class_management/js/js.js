$(document).ready(function(){
  $(".errorlist").addClass("list-unstyled");
  $(".image_class").click(function(){
    $("#id_image_class").click();
  });
  $(".image_ques").click(function(){
    $("#id_image_ques").click();
  });
      $("#id_user_image").change(function() {
            readURL($("#id_user_image"), $(".image_student"));
        });
      $("#id_image_class").change(function() {
            readURL($("#id_image_class"), $(".image_class"));
        });
      $("#id_image_ques").change(function() {
            readURL($("#id_image_ques"),$(".image_ques" ));
  });

  $('.class_in_list').hover(function(){
    $(this).find('.hover_detail').animate({top:'0px'},"slow");
  }, function(){
      $(this).find('.hover_detail').stop();
      $(this).find('.hover_detail').animate({top:'125px'},"slow");
  });
});
function readURL(input, image_input) {
    if (input.prop('files') && input.prop('files')[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            image_input.attr('src', e.target.result);
        }
        reader.readAsDataURL(input.prop('files')[0]);
        $(".del_img").show();
    }else{
    image_input.attr('src', "/media/test/img-icon.png");
  }
};

function basic_pie(container, d1, d2 , d3, d4) {
	  var  graph = Flotr.draw(container, [
    { data : d1 } ,
    { data : d2 },
    { data : d3 },
    { data : d4 }
  ], {
  	colors: ['#00A8F0', '#C0D800', '#CB4B4B', '#4DA74D', '#9440ED'],
  	ieBackgroundColor: '#FFFF',
  	fontSize: 6,
    HtmlText : false,
    grid : {
      verticalLines : false,
      horizontalLines : false,
      outlineWidth: 0
    },
    xaxis : { showLabels : false },
    yaxis : { showLabels : false },
    pie : {
      show : true, 
      explode : 1
    }
  });
};
function reset_form_element (e) {
    e.wrap('<form>').parent('form').trigger('reset');
    e.unwrap();
    };