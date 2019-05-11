$(function() {
  // Select username and email
  let username = document.querySelector(".username");
  let email = document.querySelector(".email");
  // 1. Listen for changes
  username.addEventListener("input", updateValue(username, (id = "username")));
  email.addEventListener("input", updateValue(email, (id = "email")));

  function updateValue(field, id) {
    // 2. Retrieve the text from inside the element
    document.getElementById(id).value = field.innerHTML;
  }
});
