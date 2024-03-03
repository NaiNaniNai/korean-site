var showSection = function showSection(section, isAnimate) {
  var
  direction = section.replace(/#/, ''),
  reqSection = $('.section').filter('[data-section="' + direction + '"]'),
  reqSectionPos = reqSection.offset().top - 0;

  if (isAnimate) {
    $('body, html').animate({
      scrollTop: reqSectionPos },
    800);my_file
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


function selectionExercise(exercise) {
    exercises_practical = document.querySelectorAll(".exercise_practical");
    exercises_practical.forEach(elem => {
        elem.style.display = "none";
    })
    exercise.style.display = "block";
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


function sendAnswerToBackend(button, answerId, courseSlug, moduleSlug, lessonSlug, exercisesNumber) {
    var csrftoken = getCookie("csrftoken");
    var questionDiv = button.closest('.exercise__question');
    var exerciseId = questionDiv.querySelector('input[name="exercise_id"]').value;
    var progressBar = document.querySelector(".practical_part_completed_exercises");
    var countOfExercises = document.querySelector(".practical_part_exercises_count");
    var exerciseList = $(`#exercise__title__${exercisesNumber}`);
    var exerciseMessage = $(`#exercise__message__${exercisesNumber}`);

    exerciseMessage.removeClass();
    $.ajax({
        url:`/course/${courseSlug}/${moduleSlug}/${lessonSlug}/passing`,
        type: "POST",
        data: {
            "exercises_id": exerciseId,
            "answer_id": answerId
        },
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(response) {
            if (response.success) {
                exerciseList.removeClass();
                exerciseList.addClass("exercise_practical__completed__link");
                exerciseMessage.text("Правильный ответ");
                exerciseMessage.addClass("message_success");
                var completedExercises = parseInt(progressBar.innerText);
                var countOfExercisesInt= parseInt(countOfExercises.innerText);
                if (completedExercises < countOfExercisesInt) {
                    progressBar.innerHTML = `<h4>${completedExercises+1}</h4>`;
                }
            }
            
            if (response.fail) {
                exerciseMessage.text("Неправильный ответ");
                exerciseMessage.addClass("message_error");
            }

            else {
                exerciseMessage.text("Правильный ответ");
                exerciseMessage.addClass("message_success");
            }
        }
    });
}
