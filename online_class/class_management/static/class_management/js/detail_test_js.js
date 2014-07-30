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
    $("#done_text").click(function() {
        $('#testlist').children().unbind();
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
    $('#del_text').click(function() {


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

var updatequestion = function() {
    var data = new FormData($('form').get(0));
    data.append('id', $("#id").val());
    $.ajax({
        type: "POST",
        url: "{% url 'classes:updatequestion' chosen_test.pk %}",
        dataType: "json",
        data: data,
        processData: false,
        contentType: false,
        success: function(question_dict) {
            var mom = $("#" + question_dict['id']);
            mom.find(".id_question_test").html(question_dict['question']);
            mom.find(".id_answerA_test").html(question_dict['answerA']);
            mom.find(".id_answerB_test").html(question_dict['answerB']);
            mom.find(".id_answerC_test").html(question_dict['answerC']);
            mom.find(".id_answerD_test").html(question_dict['answerD']);
            mom.find(".id_right_answer_test").html(question_dict['right_answer']);
            if (question_dict['image_ques']) {
                mom.children('img').attr('src', question_dict['image_ques']).attr('height', '150').attr('width', '150');
            } else {

                mom.children('img').attr('src', "#").attr('height', '0').attr('width', '0');
            }
        },
        error: function(errors_dict) {
            var errors = JSON.parse(errors_dict.responseText);
            $('.errorlist').remove();
            for (error in errors) {
                var id = '#id_' + error;
                console.log(id);
                $(id).parent().append(errors[error]);
            }
        }
    });
    return false;
};

var addquestion = function() {
    var data = new FormData($('form').get(0));
    $.ajax({
        type: "POST",
        url: "{% url 'classes:createtest' chosen_class.pk chosen_lesson.pk chosen_test.pk %}",
        dataType: "json",
        data: data,
        processData: false,
        contentType: false,
        success: function(question_dict) {
            var html = "<div>" + "<span class='id_test'>" + question_dict['order_test'] + "</span><span>. </span><span> class='id_question_test'>" + question_dict['question'] + "</div>";
            if (question_dict['image_ques']) {
                html += "<img src = '" + question_dict['image_ques'] + "' height=150 width=150 />";
            } else {
                html += "<img src = '#' height=0 width=0 />";
            }
            html += "<ol style='list-style-type: upper-alpha'>" + "<li class='id_answerA_test'>" + question_dict['answerA'] + "</li>" + "<li class='id_answerB_test'>" + question_dict['answerB'] + "</li>" + "<li class='id_answerC_test'>" + question_dict['answerC'] + "</li>" + "<li class='id_answerD_test'>" + question_dict['answerD'] + "</li>" + "</ol>" + "<div> Dap An Dung: <span class='id_right_answer_test'>" + question_dict['right_answer'] + "</span></div>";
            $("#testlist").append(html);
        },
        error: function(errors_dict) {
            var errors = JSON.parse(errors_dict.responseText);
            $('.errorlist').remove();
            for (error in errors) {
                var id = '#id_' + error;
                console.log(id);
                $(id).parent().append(errors[error]);
            }
        }
    });
    return false;
};