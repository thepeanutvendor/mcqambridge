const YEAR_MIN = 18;
const YEAR_MAX = 25;
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const flag = `${urlParams.get('flag')}`

function reportError(message) {
  document.getElementById("error-message").textContent = message;
  document.getElementById("error-message").hidden = false;
}

if (flag === 'False') {
  reportError('This PDF does not exist!');
}

function handleSubjectChange() {
  subjectElement = document.getElementById("subject");
  asLevel = document.getElementById("as-level");
  a2Level = document.getElementById("a2-level");
  extended = document.getElementById("extended");

  extended.disabled = ![
    "0625",
    "0620",
    "0610",
    "0653",
  ].includes(subjectElement.value);

  isAsAlevel = false;

  if (subjectElement.value === "9708") {
    isAsAlevel = true;
  }
  asLevel.disabled = !isAsAlevel;
  a2Level.disabled = !isAsAlevel;

  if (!isAsAlevel) {
    asLevel.checked = true;
  }
}

function handleMonthChange() {
  monthElement = document.querySelector("input[name=month]:checked");
  alevelElement = document.querySelector("input[name=alevel]:checked");
  subjectElement = document.getElementById("subject");
  yearElement = document.getElementById("year");
  subjectGroup = subjectElement.selectedOptions[0].parentElement.label;
}

document.getElementById("main-form").addEventListener("submit", (e) => {
  subjectValue = document.getElementById("subject").value;
  yearValue = document.getElementById("year").value;
  monthValue = document.querySelector("input[name=month]:checked").value;

  if (
    subjectValue === "please-select" ||
    yearValue === "" ||
    monthValue === ""
  ) {
    e.preventDefault(); // Prevent the form submission
    reportError("Please fill in all required fields!");
  }
});

document.getElementById("subject").addEventListener("change", () => {
  handleSubjectChange();
  handleMonthChange();
});

document.querySelectorAll("input[name=month]").forEach((monthInput) => {
  monthInput.addEventListener("change", () => {
    handleMonthChange();
  });
});
