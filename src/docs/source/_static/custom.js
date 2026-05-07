// _static/custom.js
document.addEventListener("DOMContentLoaded", function() {
  var links = document.querySelectorAll("a.external");
  links.forEach(function(link) {
    link.setAttribute("target", "_blank");
    link.setAttribute("rel", "noopener noreferrer");
  });
});