function loadNavbar() {
  fetch("/client/assets/nav/nav.html")
    .then(res => res.text())
    .then(html => {
      document.getElementById("navbar-root").innerHTML = html;
    })
    .catch(err => console.error("Failed to load navbar:", err));

  const userProfile = JSON.parse(localStorage.getItem("userProfile") || "null");

      if (!userProfile || !userProfile.full_name || !userProfile.email) {
        
        const manageBtn = document.getElementById("manage-profile-btn");
        if (manageBtn) manageBtn.style.display = "none";
      }
  }
function toggleTheme() {
  document.documentElement.classList.toggle("dark");
}

document.addEventListener("DOMContentLoaded", loadNavbar);



