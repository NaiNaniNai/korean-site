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

function SendToBackend(courseSlug, moduleSlug, lessonSlug) {
    var csrftoken = getCookie("csrftoken");
    var exerciseElements = document.querySelectorAll('.exercise_theory__title');
    var exercisesId = [];

    exerciseElements.forEach(function(element) {
        var exerciseId = element.getAttribute('id');
        exercisesId.push(exerciseId);
    });

    var progressBar = document.querySelector(".theory_part_completed_exercises");
    var countOfExercises = document.querySelector(".theory_part_exercises_count");

    $.ajax({
        url:`/course/${courseSlug}/${moduleSlug}/${lessonSlug}/passing`,
        type: "POST",
        data: {
            "exercises_id": `${exercisesId}`
        },
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function(response) {
            if (response.success) {
                var completedExercises = parseInt(progressBar.innerText);
                var countOfExercisesInt= parseInt(countOfExercises.innerText);
                if (completedExercises < countOfExercisesInt) {
                    progressBar.innerHTML = `<h4>${completedExercises+countOfExercisesInt}</h4>`;
                }
            }
        }
    });
}
