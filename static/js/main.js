document.addEventListener("DOMContentLoaded", function() {
    const navOpen = document.getElementById("nav-mobile-icon");
    const navClose = document.getElementById("navClose");
    const mainNav = document.getElementById("mainNav");


    navOpen.addEventListener("click", function() {
        mainNav.classList.add("active"); // ✅ Toggle active class
    });
    navClose.addEventListener("click", function() {
        mainNav.classList.remove("active"); // ✅ Toggle active class
    });
    
});

function adjustMainMargin() {
  const header = document.querySelector("header");
  const main = document.querySelector("main");

  if (header && main) {
    const headerHeight = header.offsetHeight -1;
    main.style.marginTop = `${headerHeight}px`;
  }
}

// Run on initial load
window.addEventListener("DOMContentLoaded", adjustMainMargin);

// Run on resize to keep it responsive
window.addEventListener("resize", adjustMainMargin);
