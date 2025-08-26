function setupSumupToggle() {
  const sumupLink = document.getElementById("sumupLink");
  const bookAnother = document.getElementById("bookAnother");

  if (!sumupLink || !bookAnother) return;

  sumupLink.addEventListener("click", () => {
    sumupLink.classList.remove("active");
    bookAnother.classList.add("active");
  });
}

document.addEventListener("DOMContentLoaded", setupSumupToggle);
