function validateForm() {}

function validate(event) {
  v = document.getElementById("email").value;

  if (v.indexOf("@") == -1) {
    event.preventDefault();
    alert("enter a valid email");
    return false;
  }

  return true;
}

function show_thankyou(article, response) {
  var div = document.createElement("div");
  div.class = "message";
  div.innerHTML = "Thank you for liking.";
  article.parentNode.appendChild(div);
}
function send_like(event) {
  article = event.target;
  article_id = article.dataset.article_id;

  fetch("/article_like/" + article_id)
    .then((response) => show_thankyou(article, response))
    // .then((response) => alert(response))
    .catch((err) => console.log(err));
}

function initialize() {
  like_buttons = document.querySelectorAll(".like-icon");
  for (const like_button of like_buttons) {
    like_button.onclick = send_like;
  }
}

var myModal = document.getElementById("myModal");
var myInput = document.getElementById("myInput");

myModal.addEventListener("shown.bs.modal", function () {
  myInput.focus();
});
