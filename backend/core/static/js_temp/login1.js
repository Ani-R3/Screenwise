document.getElementById("loginForm").addEventListener("submit", function (e) {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();
  const errorMsg = document.getElementById("error-msg");

  if (!username || !password) {
    e.preventDefault(); // stop form submission
    errorMsg.textContent = "Username and password are required.";
  }
});
