function loadNavbar() {
  fetch("/client/assets/nav/footer.html")
    .then(res => res.text())
    .then(html => {
      document.getElementById("footer-root").innerHTML = html;
    })
    .catch(err => console.error("Failed to load footer:", err));
}