$(document).ready(function(){
  $("#id_image_class").hide();
  $('label[for="id_image_class"]').hide();
  $('.browse').click(function(){
    $("#id_image_class").click();
  });
});

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