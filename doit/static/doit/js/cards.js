
// lazy load
// import Vue from 'vue';
// import 'beautify-scrollbar/dist/index.css';
// import V2LazyList from 'v2-lazy-list';



// make sure we send csrf django token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// for reminders time picker
$(function() {

    $('#id_reminder_time').on('apply.daterangepicker', function(ev, picker) {
        $(this).val(picker.startDate.format('YYYY-MM-DD HH:mm'));
    });

    $('#id_reminder_time').on('cancel.daterangepicker', function(ev, picker) {
        $(this).val('');
    });
    $('#id_reminder_time').daterangepicker({
        "singleDatePicker": true,
        "timePicker": true,
        "timePicker24Hour": true,
        "autoUpdateInput": false,
        "autoApply": true,
        "showCustomRangeLabel": false,
        locale: {
            format: 'YYYY-MM-DD HH:mm'
        }
    }, function(start, end, label) {});
});

// send reminder
function send_reminder() {
    data = $('#addreminder_form').serialize();
    console.log(data)
    $.when($.ajax({
        type: "POST",
        async: false,
        url: "/cards/addreminder/",
        data: data,
    })).then(function (data) {
        $("#addreminder_form").get(0).reset();
        $('#reminder-mess-success').removeClass('hidden');
        setTimeout(function(){
            $('#reminder-mess-success').addClass('hidden');
        }, 2000);
    });
}

// get_reminers
function get_reminders(cardid) {

    $.get( "/cards/getreminders/", { card: cardid }, function( data ) {
        if(data != null) {
            if(!$('#collapseReminders').hasClass("done")) {
                $.each(data, function(i) {
                    var div = $('<div/>');
                    div.append("<p class='' data-date=" + data[i].created_time + ">" + "<img class='user-picture' " +
                      "src=/media/"+data[i].owner+"> " + " " + data[i].reminder_time + " <a href=\"/cards/deletereminder/?reminder=" + data[i].id + "\">X</a></p>");
                    $("#collapseReminders").append(div);
                    $( ".comment:odd" ).css( "background-color", "#bbbbff" );
                    $("#collapseReminders").addClass("done")
            });
            }
        }
    });
};


// send tasks via ajax
// TODO: are we sure the comment was posted succesfully?
// when/then - then fires only when succesful so where do I catch the failures?
function send_task() {
    // TODO: check to make sure it is not empty!!!
    // assign entire form to jquery variable
    data = $('#add_task_form').serialize();
    $.when($.ajax({
        type: "POST",
        //we need this while working with mod_wsgi and apache !
        async: false,
        url: "/cards/addtask/",
        data: data,
    })).then(function (data) {
        // if so then we can clear the form
        $("#add_task_form").get(0).reset();
        // show our success message
        $('#task-mess-success').removeClass('hidden');
        // remove it after 3 secs
        setTimeout(function(){
            $('#task-mess-success').addClass('hidden');
            //....and whatever else you need to do
        }, 2000);
        // TODO: we now have to push the view tasks twice (once to collapse
        $("#collapseTasks").removeClass("done")
        $("#collapseTasks").empty()
        var card = $('#add_task_form :input[name="card"]').val();
        $.get("/cards/gettaskcount/", { card: card}, function(taskcount) {
            $(".taskcount").html(taskcount);
        });
    });
}

// get tasks for the card within modal
// it seems that we still load on every click
function get_tasks(cardid) {
    $.get( "/cards/gettasks/", { card: cardid }, function( data ) {
        if(!$('#collapseTasks').hasClass("done")) {
            $.each(data, function(i) {
              var div = $('<div class="task-list-container">');
              if(data[i].done){
                  var checked = "checked";
              } else {
                  checked = '';
              }
              div.append(
                  "<input name='task' value=" + data[i].id + " " + checked + " type='checkbox' class='task-item task-checkbox' data-date=" + data[i].created_time + ">&nbsp;<span><img class='user-picture' " +
                  "src=/media/"+data[i].owner+"> " + data[i].task + " </span>"
              );
              $("#collapseTasks").append(div);
              $("#collapseTasks").addClass("done")
            });
        }
    });
};

//<!-- tasklist tab in editcard modal -->
$(document).on('change' , '.task-checkbox' , function(){
    if(this.checked) {
        taskid = this.value;
        $.when($.ajax({
            type: "POST",
            async: false,
            url: "/cards/updatetask/",
            data: {
                task: taskid,
                status: "True",
                csrfmiddlewaretoken: csrftoken,
            },
        })).then(function (data) {
            $('#task-mess-success').removeClass('hidden');
            setTimeout(function(){
                $('#task-mess-success').addClass('hidden');
        }, 2000);

        });
    } else {
        // we unchecked a checkbox
        taskid = this.value;
        $.when($.ajax({
            type: "POST",
            async: false,
            url: "/cards/updatetask/",
            data: {
                task: taskid,
                status: "False",
                csrfmiddlewaretoken: csrftoken,
            },
        })).then(function (data) {
            // show our success message
            $('#task-mess-success').removeClass('hidden');
            // remove it after 3 secs
            setTimeout(function(){
                $('#task-mess-success').addClass('hidden');
        }, 2000);
        });
    }
});

//
// END TASKS STUFF
//


//
// submit form for editcard via ajax
//

// disable trix image uploads ..




//
// END submit form for editcard via ajax
//
