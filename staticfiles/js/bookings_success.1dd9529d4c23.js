document.addEventListener("DOMContentLoaded", function () {
  const sumupLink = document.getElementById("sumup_link");
  const bookAnother = document.getElementById("bookAnother");

  if (sumupLink && bookAnother) {
    sumupLink.addEventListener("click", function () {
      sumupLink.style.display = "none";

      bookAnother.style.display = "flex";
    });
  }
});
