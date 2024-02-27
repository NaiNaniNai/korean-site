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

function getUrl() {
    return document.getElementById("lesson_slug").textContent
};

var url = getUrl();

function handleIntersection(entries, observer) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            sendToBackend(`${entry.target.id}`, url);
        }
    });
}

const observer = new IntersectionObserver(handleIntersection);
const elements = document.querySelectorAll('.exercise_theory__title');

elements.forEach(element => {
    observer.observe(element);
});


function sendToBackend(exerciseId, url) {
    var csrftoken = getCookie("csrftoken");
    var progressBar = document.querySelector(".theory_part_completed_exercises");
    var countOfExercises = document.querySelector(".theory_part_exercises_count");

    $.ajax({
        url:`/course/${url}/passing`,
        type: "POST",
        data: {
            "exercises_id": exerciseId
        },
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(response) {
            if (response.success) {
                var completedExercises = parseInt(progressBar.innerText);
                var countOfExercisesInt= parseInt(countOfExercises.innerText);
                if (completedExercises < countOfExercisesInt) {
                    progressBar.innerHTML = `<h4>${completedExercises+1}</h4>`;
                }
            }
        }
    });
}
