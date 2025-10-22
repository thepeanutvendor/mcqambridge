var userAnswers = [];
var questionNumber = 0;
var displayNumber = 1;
const incorrectFeedback = document.getElementById("incorrect-answer");
const correctFeedback = document.getElementById("correct-answer");
const title = document.getElementById("title");
const numOfQuestions = correctAnswers.length ;

// Recording and checking answers
function answer(option) {
  userAnswers[questionNumber] = option;
  if (option === correctAnswers[questionNumber]) {
    incorrectFeedback.style.display = "none";
    correctFeedback.style.display = "block";
  } else if (option !== correctAnswers[questionNumber]) {
    correctFeedback.style.display = "none";
    incorrectFeedback.style.display = "block";
  }
  if (questionNumber === numOfQuestions - 1) {
    toPdfScore();
    return false;
  }
  questionNumber += 1;
  displayNumber += 1;
  title.textContent = `Question ${displayNumber}`;

}

function toPdfScore() {
  var form = document.getElementById("form");
  var correctAnswersInput = document.getElementById('correct-answers');
  var userAnswersInput = document.getElementById('user-answers');
  var paperNameInput = document.getElementById('paper-name');

  correctAnswersInput.setAttribute("value", correctAnswers);
  userAnswersInput.setAttribute("value", userAnswers);
  paperNameInput.setAttribute("value", document.querySelector('title').textContent);

  form.submit();
}
var qpName = document.querySelector('title').textContent.replace('ms', 'qp')

var url = `https://pastpapers.co/cie/${qpName}`;

// Alternative viewer using Google Docs Viewer
// var url = `https://docs.google.com/viewer?url=https://pastpapers.co/cie/${qpName}&embedded=true`;

document.getElementById('canvas').src = url;