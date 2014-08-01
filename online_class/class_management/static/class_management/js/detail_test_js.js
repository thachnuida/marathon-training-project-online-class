$(document).ready(function() {
    $("#id_image_ques").hide();
    $('label[for="id_image_ques"]').hide();
    $('#add_ques').hide();

    $('.browse').click(function() {
        $("#id_image_ques").click();
        $("#id_image_ques").change(function() {
            readURL($("#id_image_ques"));
        });
    });

     $('#add_text').click(function(){
        $("#edit_text").animate({
          height: '0px',
          width: '0px'
        },"slow");

        $("#del_text").animate({
          height: '0px',
          width: '0px'
        },"slow");
        $("#testlist").animate({
            'margin-left': '499px'
        }, "slow");
        $('#add_ques').show('slow');
        $('#add_question').show('slow');
        $('#update_question').hide();

    });

    
    $("#edit_text").click(function() {
        alert("Kích Vào Câu Hỏi Cần Chỉnh Sửa");
         $("#add_text").animate({
          height: '0px',
          width: '0px'
        },"slow");

        $("#del_text").animate({
          height: '0px',
          width: '0px'
        },"slow");
        
        

        $("#testlist").children().hover(function() {
            $(this).css("background-color", "#E8E8E8 ");
        }, function() {
            $(this).css('background-color', '');
        });
        $("#testlist").children().click(function() {

        $("#testlist").animate({
            'margin-left': '499px'
        }, "slow");
        $('#add_ques').show('slow');
        $('#add_question').hide();
        $('#update_question').show('slow');
            $('#id_question').html($(this).find(".id_question_test").html());
            $("#id").val($(this).find(".id_test").html());
            if ($(this).children('img').attr('src') != "#") $('#image_test').attr('src', $(this).children('img').attr('src'));
            else $('#image_test').attr('src', "/media/test/img-icon.png");
            $('#id_question').html($(this).find(".id_question_test").html());
            $('#id_answerA').html($(this).find(".id_answerA_test").html());
            $('#id_answerB').html($(this).find(".id_answerB_test").html());
            $('#id_answerC').html($(this).find(".id_answerC_test").html());
            $('#id_answerD').html($(this).find(".id_answerD_test").html());
            $("input[name=right_answer][value=" + $(this).find(".id_right_answer_test").html() + "]").prop('checked', true);
        });
    });

     $('#done_text').click(function(){
        $("#testlist").children().unbind();
        $("#add_ques").hide();
        $("#add_text").animate({
          height: '58px',
          width: '58px'
        },"slow");

        $("#del_text").animate({
          height: '58px',
          width: '58px'
        },"slow");
         $("#edit_text").animate({
          height: '58px',
          width: '58px'
        },"slow");
         $("#testlist").animate({
            'margin-left': '0px'
        }, "slow");
     });
    });


function readURL(input) {
    if (input.prop('files') && input.prop('files')[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $('#image_test').attr('src', e.target.result);
            console.log(e.target.rult);
        }
        reader.readAsDataURL(input.prop('files')[0]);
    }
};

