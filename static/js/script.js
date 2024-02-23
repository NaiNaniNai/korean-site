var showSection = function showSection(section, isAnimate) {
  var
  direction = section.replace(/#/, ''),
  reqSection = $('.section').filter('[data-section="' + direction + '"]'),
  reqSectionPos = reqSection.offset().top - 0;

  if (isAnimate) {
    $('body, html').animate({
      scrollTop: reqSectionPos },
    800);
  } else {
    $('body, html').scrollTop(reqSectionPos);
  }

};

function selectionPartOfLesson(type) {
    exercises_theory = document.querySelector(".exercises_theory");
    exercises_practical = document.querySelector(".exercises_practical");
    exercises_homework = document.querySelector(".exercises_homework");
    exercises_theory.style.display = "none";
    exercises_practical.style.display = "none";
    exercises_homework.style.display = "none";
    elem = document.querySelector('.'+ type)
    elem.style.display = "block";
}


function selectionExercise(number) {
    exercises_practical = document.querySelectorAll(".exercise_practical");
    exercises_practical.forEach(elem => {
        elem.style.display = "none";
    })
    element = document.getElementById(number);
    element.style.display = "block";
}


var startTime;
startTimer();


$(window).on("beforeunload", function() {
    sendTimeToBackend();
});

function startTimer() {
    startTime = new Date().getTime();
}


function sendTimeToBackend() {
    var currentTime = new Date().getTime();
    var onlineTime = Math.floor((currentTime - startTime) / 1000);
    var csrftoken = getCookie("csrftoken");
    $.ajax({
        url: "/update_last_online/",
        type: "POST",
        data: {
            "current_time": currentTime,
            "online_time": onlineTime
        },
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function changeVisionRating(button1, button2, rating) {
    week_activity_button = document.querySelector(".week_activity_button");
    month_activity_button = document.querySelector(".month_activity_button");
    top_rating_button = document.querySelector(".top_rating_button");
    self_rating_month = document.querySelector(".self_rating_month");
    self_rating_week = document.querySelector(".self_rating_week");
    top_rating = document.querySelector(".top_rating");

    week_activity_button.style.display = "none";
    month_activity_button.style.display = "none";
    top_rating_button.style.display = "none";
    self_rating_month.style.display = "none";
    self_rating_week.style.display = "none";
    top_rating.style.display = "none";

    button = document.querySelector('.rating_button')
    button1 = document.querySelector('.'+ button1)
    button2 = document.querySelector('.'+ button2)
    rating = document.querySelector('.' + rating)
    button.style.display = "flex";
    button1.style.display = "block";
    button2.style.display = "block";
    button2.style.marginLeft = "5px";
    rating.style.display = "block";
}


function sendAnswerToBackend(button, courseSlug, moduleSlug, lessonSlug) {
    var csrftoken = getCookie("csrftoken");
    var questionDiv = button.closest('.exercise__question');
    var selectedAnswer = questionDiv.querySelector('input[name="answer_id"]:checked');
    if (!selectedAnswer) {
        alert("Не выбран ответ!");
    }
    else {
        var exerciseId = questionDiv.querySelector('input[name="exercise_id"]').value;
        var answerId = selectedAnswer.value;
        console.log(`${courseSlug}/${moduleSlug}/${lessonSlug}/passing`);
        $.ajax({
            url:`/course/${courseSlug}/${moduleSlug}/${lessonSlug}/passing`,
            type: "POST",
            data: {
                "exercise_id": exerciseId,
                "answer_id": answerId
            },
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function(response) {
                if (response.success) {
                    $("#exercise__message").text("Правильный ответ");
                    $("#exercise__message").removeClass();
                    $("#exercise__message").addClass("message_success");

                }
                else {
                    $("#exercise__message").text("Неправильный ответ");
                    $("#exercise__message").removeClass();
                    $("#exercise__message").addClass("message_error");
                }
            }
        });
    }
}
