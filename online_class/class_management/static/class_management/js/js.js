$(document).ready(function(){
  $(".dropdown").hover(function(){
    $(".dropdown-menu").show();
  }, function(){
    $(".dropdown-menu").hide();
  });
      $("#id_image_class").change(function() {
            readURL($("#id_image_class"), $("#image_class"));
        });
      $("#id_image_ques").change(function() {
            readURL($("#id_image_ques"),$("#image_ques" ));
  });

  $('.class_in_list').hover(function(){
    $(this).find('.hover_detail').animate({top:'0px'},"slow");
  }, function(){
      $(this).find('.hover_detail').stop();
      $(this).find('.hover_detail').animate({top:'140px'},"slow");
  });

  $(".lesson_wrapper").hover(function(){
    $(this).css("background-color", 'rgb(192, 188, 190)');
  }, function(){
    $(this).css("background-color", '');
  });

});

function readURL(input, image_input) {
    if (input.prop('files') && input.prop('files')[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            image_input.attr('src', e.target.result);
        }
        reader.readAsDataURL(input.prop('files')[0]);
    }
    image_input.attr('src', "/media/test/img-icon.png");
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