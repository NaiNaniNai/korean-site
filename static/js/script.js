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
