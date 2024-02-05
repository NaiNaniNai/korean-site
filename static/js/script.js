$('.nav li:first').addClass('active');

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

var checkSection = function checkSection() {
  $('.section').each(function () {
    var
    $this = $(this),
    topEdge = $this.offset().top - 80,
    bottomEdge = topEdge + $this.height(),
    wScroll = $(window).scrollTop();
    if (topEdge < wScroll && bottomEdge > wScroll) {
      var
      currentId = $this.data('section'),
      reqLink = $('a').filter('[href*=\\#' + currentId + ']');
      reqLink.closest('li').addClass('active').
      siblings().removeClass('active');
    }
  });
};

$('.main-menu, .responsive-menu, .scroll-to-section').on('click', 'a', function (e) {
  e.preventDefault();
  showSection($(this).attr('href'), true);
});

$(window).scroll(function () {
  checkSection();
});

//
//$('lesson_plan_part_exercise__title').on('click', 'a', callbackHandler);
//const scrollTopCoordinate = $("#header").offset().top - $(window).height()*0.02
//$([document.documentElement, document.body]).animate({
//scrollTop: scrollTopCoordinate
//}, 2000);
$("#test_1").click(callbackHandler);
$([document.documentElement, document.body]).animate({
scrollTop: scrollTopCoordinate
}, 2000);
const scrollTopCoordinate = $("#header").offset().top - $(window).height() * 0.02

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
