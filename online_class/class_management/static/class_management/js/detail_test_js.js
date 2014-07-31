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
        $('#add_ques').show();
        $('#add_question').show();
        $('#update_question').hide();

    });

    
    $("#edit_text").click(function() {
        alert("Kich vao kfasdjf");
        $("#testlist").children().hover(function() {
            $(this).css("background-color", "#E8E8E8 ");
        }, function() {
            $(this).css('background-color', '');
        });
        $("#testlist").children().click(function() {
            $('#add_ques').show();
            $('#update_question').show();
            $("#add_question").hide();
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

